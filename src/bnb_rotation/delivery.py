"""Local human review and delivery plans; never upload, submit or sign."""
import hashlib
import json
import re
import time
from contextlib import contextmanager
from pathlib import Path

from .service import fingerprint, utc
from .termix import AGENT_ID, binding, checked_order, order_id


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def atomic_json(path, value):
    temporary = path.with_suffix(".tmp")
    try:
        with temporary.open("x", encoding="utf-8") as stream:
            json.dump(value, stream, indent=2, allow_nan=False)
            stream.write("\n")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


@contextmanager
def job_lock(queue_dir, identifier):
    root = Path(queue_dir)
    identifier = order_id(identifier)
    job = root / identifier
    if not job.is_dir() or job.is_symlink():
        raise ValueError("queued draft not found")
    lock = root / (identifier + ".lock")
    try:
        lock.mkdir(mode=0o700)
    except FileExistsError:
        raise ValueError("order is already being processed") from None
    try:
        yield job
    finally:
        lock.rmdir()


def verified_manifest(job, identifier):
    path = job / "manifest.json"
    manifest = json.loads(path.read_text())
    if (manifest.get("chain_id") != 56 or manifest.get("agent_id") != AGENT_ID
            or manifest.get("order", {}).get("id") != identifier
            or manifest.get("status") != "DRAFT_REQUIRES_OPERATOR_REVIEW"
            or manifest.get("delivery_submitted") is not False):
        raise ValueError("invalid draft manifest")
    hashes = manifest.get("artifact_sha256")
    if not isinstance(hashes, dict) or set(hashes) != {"report.md", "report.json"}:
        raise ValueError("invalid draft artifact manifest")
    for name, expected in hashes.items():
        artifact = job / name
        if artifact.is_symlink() or sha256(artifact.read_bytes()) != expected:
            raise ValueError("draft artifact changed; review required")
    return manifest, sha256(path.read_bytes())


def current_order(reader, manifest, now_ms):
    live = checked_order(reader, manifest["order"]["id"], max(now_ms, int(time.time() * 1000)))
    if binding(live) != manifest["order"]:
        raise ValueError("order changed since draft; review required")
    return live


def review_copy(reader, queue_dir, identifier, now_ms):
    """Create an editable copy; no approval is inferred from this command."""
    identifier = order_id(identifier)
    with job_lock(queue_dir, identifier) as job:
        manifest, _ = verified_manifest(job, identifier)
        current_order(reader, manifest, now_ms)
        review = job / "review"
        review.mkdir(exist_ok=True, mode=0o700)
        if review.is_symlink():
            raise ValueError("review directory must be local")
        path = review / "report.md"
        if path.is_symlink():
            raise ValueError("review file must be local")
        if not path.exists():
            # Keep the draft and its limitations verbatim. The operator may
            # revise this copy, including its draft labels, before approval.
            path.write_bytes((job / "report.md").read_bytes())
        return {"status": "AWAITING_OPERATOR_REVIEW", "order_id": identifier,
                "review_file": str(path), "report_sha256": sha256(path.read_bytes())}


def approve_report(reader, queue_dir, identifier, expected_sha256, reviewer, note, now_ms):
    """Record the human's approval of exact bytes and current order identity."""
    if not isinstance(expected_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
        raise ValueError("approval requires the exact report SHA-256")
    if any(not isinstance(v, str) or not v.strip() or len(v) > 1000 for v in (reviewer, note)):
        raise ValueError("reviewer and review note required")
    identifier = order_id(identifier)
    with job_lock(queue_dir, identifier) as job:
        manifest, manifest_hash = verified_manifest(job, identifier)
        current_order(reader, manifest, now_ms)
        path = job / "review/report.md"
        if path.is_symlink() or path.parent.is_symlink():
            raise ValueError("review file must be local")
        content = path.read_bytes()
        if not content.strip() or sha256(content) != expected_sha256:
            raise ValueError("reviewed report changed or is empty")
        approval = {"status": "OPERATOR_APPROVED", "order_id": identifier,
                    "job_sha256": manifest["job_sha256"], "manifest_sha256": manifest_hash,
                    "report_sha256": expected_sha256, "reviewer": reviewer.strip(),
                    "review_note": note.strip(), "approved_at_utc": utc(now_ms)}
        atomic_json(job / "approval.json", approval)
        # A new approval invalidates any older plan.
        (job / "delivery-plan.json").unlink(missing_ok=True)
        return approval


def prepare_delivery(reader, queue_dir, identifier, now_ms):
    """Build a local API handoff plan, stopping before upload or transaction."""
    identifier = order_id(identifier)
    with job_lock(queue_dir, identifier) as job:
        # A failed new check must not leave a previous success-looking plan.
        (job / "delivery-plan.json").unlink(missing_ok=True)
        manifest, manifest_hash = verified_manifest(job, identifier)
        approval = json.loads((job / "approval.json").read_text())
        if (approval.get("status") != "OPERATOR_APPROVED" or approval.get("order_id") != identifier
                or approval.get("job_sha256") != manifest.get("job_sha256")
                or approval.get("manifest_sha256") != manifest_hash):
            raise ValueError("approval is missing or does not bind this draft")
        report = job / "review/report.md"
        if report.is_symlink() or report.parent.is_symlink():
            raise ValueError("review file must be local")
        content = report.read_bytes()
        checksum = sha256(content)
        if checksum != approval.get("report_sha256"):
            raise ValueError("approved report changed; approve again")
        current_order(reader, manifest, now_ms)
        base = "/api/v1/orders/" + identifier + "/delivery"
        plan = {"status": "READY_FOR_OPERATOR_DELIVERY", "chain_id": 56,
                "order_id": identifier, "escrow_contract": manifest["order"]["escrowContract"],
                "approval_sha256": fingerprint(approval), "checked_at_utc": utc(now_ms),
                "file": {"path": str(report.resolve()), "contentType": "text/markdown",
                         "sizeBytes": len(content), "sha256": "0x" + checksum},
                "steps": [
                    {"method": "POST", "path": base + "/upload-url",
                     "body": {"fileName": "report.md", "contentType": "text/markdown", "sizeBytes": len(content)}},
                    {"method": "PUT", "url_from": "upload-url.uploadUrl", "file": "approved report.md"},
                    {"method": "POST", "path": base + "/artifacts",
                     "body": {"s3Key": "$upload.s3Key", "url": "$upload.publicUrl",
                              "sha256": "0x" + checksum, "contentType": "text/markdown", "sizeBytes": len(content)}},
                    {"method": "POST", "path": base + "/submit",
                     "body": {"artifactIds": ["$registeredArtifact.id"], "note": "Operator-reviewed research report"}},
                    {"action": "VERIFY_UNSIGNED_INTENT_AND_REQUEST_WEB_WALLET_SIGNATURE"},
                    {"method": "GET", "path": "/api/v1/orders/" + identifier,
                     "required_indexed_status": "DELIVERED"}],
                "requires_recheck_before_upload_and_submit": True,
                "uploaded": False, "transaction_prepared": False,
                "signed": False, "delivery_submitted": False}
        atomic_json(job / "delivery-plan.json", plan)
        return {"status": plan["status"], "order_id": identifier,
                "plan_file": str(job / "delivery-plan.json"), "delivery_submitted": False}


def validate_delivery_intent(plan, intent):
    """Guard the real API intent before handing it to wallet signing."""
    if (plan.get("status") != "READY_FOR_OPERATOR_DELIVERY" or plan.get("chain_id") != 56
            or not re.fullmatch(r"0x[0-9a-fA-F]{40}", str(plan.get("escrow_contract")))
            or intent.get("action") != "submitDelivery" or type(intent.get("chainId")) is not int
            or intent["chainId"] != 56 or intent.get("value") != "0"
            or not isinstance(intent.get("contract"), str)
            or intent["contract"].lower() != str(plan.get("escrow_contract")).lower()
            or not re.fullmatch(r"0x[0-9a-fA-F]+", str(intent.get("callData")))
            or len(intent["callData"]) < 10 or len(intent["callData"]) % 2):
        raise ValueError("unexpected delivery transaction intent")
    # This envelope check is not a decoded calldata/simulation approval.
    # The wallet must simulate and review the actual call before signing.
    return {"status": "REQUIRES_WALLET_SIMULATION_AND_SIGNATURE", "chain_id": 56}
