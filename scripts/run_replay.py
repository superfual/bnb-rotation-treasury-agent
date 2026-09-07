import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from bnb_rotation.demo import deterministic_market
from bnb_rotation.replay import walk_forward_replay

config = json.loads((ROOT / "config/watchlist.json").read_text())
market = deterministic_market(config["candidates"], count=180)
decision_times = [c.close_time for c in market[config["benchmark"]]][89:]
result = walk_forward_replay(market, decision_times, config, fee_rate=0.001)

print("WALK-FORWARD REPLAY")
print(f"Method: {result['method']}")
print(f"Periods: {result['periods']}")
for name, metrics in [("strategy", result["strategy"]), *result["benchmarks"].items()]:
    print(f"{name}: return={metrics['cumulative_return']:.2%} max_drawdown={metrics['maximum_drawdown']:.2%}")
print(f"Research gate: {result['viability']['status']}")
print(f"Blockers: {', '.join(result['viability']['blockers']) or 'none'}")
