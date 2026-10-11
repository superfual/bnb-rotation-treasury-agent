"""Generate a local research draft from a host-injected Binance MCP snapshot."""
import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from bnb_rotation.service import build_report, render_markdown


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = build_report(json.loads(args.snapshot.read_text()), json.loads(args.request.read_text()),
                              json.loads((ROOT / "config/watchlist.json").read_text()), int(time.time() * 1000))
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 1
    # Blocked inputs never write a success-looking artifact.
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / "report.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    (args.output / "report.md").write_text(render_markdown(report))
    print(json.dumps({"status": report["status"], "request_id": report["request"]["request_id"],
                      "output": str(args.output), "bnb_regime": report["analysis"]["bnb_regime"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
