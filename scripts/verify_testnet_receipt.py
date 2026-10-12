"""Write receipt evidence only after verifying a real reviewed testnet transaction."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from bnb_rotation.onchain import RPC, verify_receipt

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--plan", type=Path, required=True)
parser.add_argument("--tx-hash", required=True)
parser.add_argument("--rpc", required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
try:
    if args.output.exists():
        raise ValueError("evidence already exists")
    result = verify_receipt(json.loads(args.plan.read_text()), args.tx_hash, RPC(args.rpc))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as output:
        json.dump(result, output, indent=2)
    print(json.dumps(result))
except (ValueError, KeyError, TypeError, OSError):
    print("BLOCKED: receipt absent, failed or mismatched; no execution evidence written", file=sys.stderr)
    sys.exit(1)
