"""Read-only TermiX order intake. No runtime polling or marketplace mutations."""
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

from .service import build_report, fingerprint, render_markdown, validate_request

AGENT_ID = "cmv272a0kg4y8zw01sg7tclan"
LISTING_ID = "cmv2uos8s0grdwx01t9j48xdi"


def order_id(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,100}", value):
        raise ValueError("invalid order ID")
    return value


class TermixReader:
    def __init__(self, skill_dir, credential_workdir):
        self.script = Path(skill_dir).resolve() / "scripts/aacp-api.mjs"
        self.workdir = Path(credential_workdir).resolve()
        if not self.script.is_file():
            raise ValueError("TermiX API helper not found")

    def get(self, path):
        env = dict(os.environ, AACP_CHAIN="bsc")
        # A base override could silently select another marketplace.
        env.pop("AACP_BASE_URL", None)
        result = subprocess.run(["node", str(self.script), "GET", path, "--auth", "session"],
                                cwd=self.workdir, env=env, capture_output=True, text=True,
                                timeout=60)
        if result.returncode:
            # Never propagate helper stderr, which may contain credentials.
            raise ValueError("TermiX read failed; check account link and connectivity")
        return json.loads(result.stdout)

    def orders(self):
        items, page = [], 1
        while page <= 1000:
            query = urlencode(dict(side="provider", providerAgentId=AGENT_ID,
                                   listingId=LISTING_ID, pageSize=100, page=page))
            response = self.get("/api/v1/orders?" + query)
            if not isinstance(response, dict):
                raise ValueError("unsupported TermiX order-list schema")
            rows, total = response.get("items"), response.get("totalPages")
            if not isinstance(rows, list) or type(total) is not int or total < 0:
                raise ValueError("unsupported TermiX order-list schema")
            if any(not isinstance(row, dict) or not isinstance(row.get("id"), str) for row in rows):
                raise ValueError("unsupported TermiX order-list row")
            items.extend(rows)
            if page >= total:
                return items
            page += 1
        raise ValueError("order pagination exceeded limit")

    def detail(self, identifier):
        return self.get("/api/v1/orders/" + order_id(identifier))


def readiness(order, now_ms):
    status = order.get("status")
    if status == "PENDING_ACCEPT":
        return "NEEDS_WALLET_ACCEPTANCE"
    if status not in {"FUNDED", "IN_PROGRESS"}:
        return "NOT_READY"
    due = order.get("deliveryDueAt")
    try:
        deadline = datetime.fromisoformat(due.replace("Z", "+00:00"))
        if deadline.tzinfo is None:
            raise ValueError("timezone required")
    except (ValueError, AttributeError, TypeError):
        return "MISSING_OR_INVALID_DEADLINE"
    if deadline.timestamp() * 1000 <= now_ms:
        return "DELIVERY_EXPIRED"
    actions = order.get("availableActions")
    if not isinstance(actions, dict) or actions.get("canSubmitDelivery") is not True:
        return "DELIVERY_NOT_AUTHORIZED"
    return "READY_FOR_DRAFT"


def binding(order):
    return {key: order.get(key) for key in
            ("id", "chainOrderId", "escrowContract", "listingId", "status",
             "budget", "currency", "deliveryDueAt", "redoUsed", "title",
             "offerId", "prepaymentOrderId")}


def checked_order(reader, identifier, now_ms):
    # Membership is established by the authenticated, agent/listing-filtered
    # provider list. Public detail alone does not establish ownership.
    if identifier not in {row.get("id") for row in reader.orders()}:
        raise ValueError("order is not in this agent's authenticated provider listing")
    order = reader.detail(identifier)
    if not isinstance(order, dict):
        raise ValueError("unsupported TermiX order-detail schema")
    if order.get("id") != identifier or order.get("listingId") != LISTING_ID:
        raise ValueError("order identity or listing mismatch")
    if not order.get("chainOrderId") or not order.get("escrowContract"):
        raise ValueError("missing indexed on-chain order identity")
    ready = readiness(order, now_ms)
    if ready != "READY_FOR_DRAFT":
        raise ValueError(ready)
    return order


def queue_draft(reader, intake, snapshot, config, queue_dir, now_ms):
    if set(intake) != {"order_id", "scope_reviewed", "request"} or intake["scope_reviewed"] is not True:
        raise ValueError("operator-reviewed structured intake required")
    identifier = order_id(intake["order_id"])
    request = validate_request(intake["request"])
    if request["request_id"] != identifier:
        raise ValueError("request_id must match the real order ID")
    order = checked_order(reader, identifier, now_ms)
    identity = fingerprint({"chain_id": 56, "agent_id": AGENT_ID,
                            "order": binding(order), "intake": intake, "config": config})
    root = Path(queue_dir)
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    target = root / identifier
    lock = root / (identifier + ".lock")
    try:
        lock.mkdir(mode=0o700)
    except FileExistsError:
        raise ValueError("order is already being processed; inspect lock before retry") from None
    temporary = None
    try:
        if target.exists():
            manifest = json.loads((target / "manifest.json").read_text())
            if manifest.get("job_sha256") != identity:
                raise ValueError("existing draft has changed order, intake or config; review required")
            for name, expected in manifest["artifact_sha256"].items():
                if hashlib.sha256((target / name).read_bytes()).hexdigest() != expected:
                    raise ValueError("existing draft artifact changed; review required")
            return {"status": "ALREADY_QUEUED", "order_id": identifier, "output": str(target)}
        report = build_report(snapshot, request, config, now_ms)
        # Re-read authoritative membership/state after calculation.
        latest = checked_order(reader, identifier, int(datetime.now(timezone.utc).timestamp() * 1000))
        if binding(latest) != binding(order):
            raise ValueError("order changed during analysis; no draft queued")
        temporary = Path(tempfile.mkdtemp(prefix=".draft-", dir=root))
        (temporary / "report.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
        (temporary / "report.md").write_text(render_markdown(report))
        artifacts = {name: hashlib.sha256((temporary / name).read_bytes()).hexdigest()
                     for name in ("report.json", "report.md")}
        manifest = {"status": "DRAFT_REQUIRES_OPERATOR_REVIEW", "chain_id": 56,
                    "agent_id": AGENT_ID, "order": binding(order), "job_sha256": identity,
                    "artifact_sha256": artifacts, "snapshot_sha256": fingerprint(snapshot),
                    "delivery_submitted": False}
        (temporary / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
        temporary.rename(target)
        temporary = None
        return {"status": manifest["status"], "order_id": identifier, "output": str(target)}
    finally:
        if temporary is not None:
            shutil.rmtree(temporary)
        lock.rmdir()
