"""Inspect provider orders or queue a local report for operator review."""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from bnb_rotation.termix import TermixReader, queue_draft, readiness


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--credential-workdir", type=Path, required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("inspect")
    draft = sub.add_parser("draft")
    draft.add_argument("--intake", type=Path, required=True)
    draft.add_argument("--snapshot", type=Path, required=True)
    draft.add_argument("--queue", type=Path, default=ROOT / "service-local/queue")
    args = parser.parse_args()
    try:
        reader = TermixReader(args.skill_dir, args.credential_workdir)
        now = int(time.time() * 1000)
        if args.command == "inspect":
            items = reader.orders()
            result = {"chain_id": 56, "order_count": len(items), "orders": []}
            for row in items:
                detail = reader.detail(row["id"])
                result["orders"].append({"order_id": row["id"], "status": detail.get("status"),
                                         "readiness": readiness(detail, now)})
        else:
            result = queue_draft(reader, json.loads(args.intake.read_text()),
                                 json.loads(args.snapshot.read_text()),
                                 json.loads((ROOT / "config/watchlist.json").read_text()), args.queue, now)
        print(json.dumps(result))
        return 0
    except (ValueError, KeyError, TypeError, OSError, subprocess.TimeoutExpired):
        # Keep marketplace/customer data and helper output out of error logs.
        print("BLOCKED: check order readiness, reviewed intake, snapshot and local queue state", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
