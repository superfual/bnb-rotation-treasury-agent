"""Read BSC testnet, simulate, and write an owner-reviewed unsigned transaction."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from bnb_rotation.onchain import RPC, build_plan


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--rpc", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("use a new output path; stale plans must not be reused")
    plan = build_plan(json.loads(args.policy.read_text()), RPC(args.rpc))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(plan, indent=2) + "\n")
    print(json.dumps({"status": plan["status"], "chain_id": plan["chain_id"], "executed": False}))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError):
        print("BLOCKED: check verified testnet policy, RPC state, balance and simulation", file=sys.stderr)
        sys.exit(1)
