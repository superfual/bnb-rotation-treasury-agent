import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
live = json.loads((ROOT / "evidence/live_summary.json").read_text())
replay = json.loads((ROOT / "evidence/replay_summary.json").read_text())

if live["raw_snapshot_sha256"] != replay["snapshot_sha256"]:
    raise SystemExit("BLOCKED: EVIDENCE_HASH_MISMATCH")
if live["mode"] != "READ_ONLY":
    raise SystemExit("BLOCKED: EVIDENCE_NOT_READ_ONLY")

full = replay["full_sample"]
experiment = replay["experiment_viability"]

print("BNB ROTATION & TREASURY — VERIFIED CONTROL ROOM")
print("Mode: PAPER ONLY | Exchange orders: DISABLED")
print(f"Evidence: Binance MCP READ_ONLY | SHA256: {replay['snapshot_sha256']}")
print(f"Current regime: {live['bnb_regime']} | Paper action: {live['portfolio']['action']}")
print(f"Current shock blockers: {', '.join(live['shock_blockers']) or 'none'}")
print("\n409-PERIOD FULL SAMPLE")
print(f"Strategy: {full['strategy']['cumulative_return']:.2%} | max DD: {full['strategy']['maximum_drawdown']:.2%}")
print(f"BNB hold: {full['benchmarks']['bnb_hold']['cumulative_return']:.2%} | max DD: {full['benchmarks']['bnb_hold']['maximum_drawdown']:.2%}")
print("\nFROZEN CHRONOLOGICAL SPLITS")
for name in ("train", "validation", "holdout"):
    result = replay["splits"][name]
    print(
        f"{name.upper():10} periods={result['periods']:>3} "
        f"strategy={result['strategy']['cumulative_return']:>7.2%} "
        f"BNB={result['benchmarks']['bnb_hold']['cumulative_return']:>7.2%} "
        f"maxDD={result['strategy']['maximum_drawdown']:>6.2%}"
    )
print(f"\nExperiment gate: {experiment['status']}")
print(f"Blockers: {', '.join(experiment['blockers']) or 'none'}")
print("Final authority: PAPER RESEARCH ONLY — NO LIVE EXECUTION")
