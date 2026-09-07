import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from bnb_rotation.binance import histories_from_snapshot
from bnb_rotation.pipeline import run_pipeline

path=ROOT/"evidence/live_snapshot.json"; raw=path.read_bytes(); snapshot=json.loads(raw)
config=json.loads((ROOT/"config/watchlist.json").read_text())
result=run_pipeline(histories_from_snapshot(snapshot),snapshot["decision_time_utc_ms"],config)
print("LIVE BINANCE MCP EVIDENCE — READ ONLY")
print(f"Snapshot SHA256: {hashlib.sha256(raw).hexdigest()}")
print(f"Decision time: {snapshot['decision_time_utc_ms']} UTC-ms")
print(f"Preflight: {result['status']} | common closed candles: {result.get('closed_candles_per_symbol',0)}")
if result["status"]!="READY":
    print(f"BLOCKED: {result['reason']}"); raise SystemExit(1)
print(f"BNB regime: {result['bnb_regime']} | blockers: {', '.join(result['regime_blockers']) or 'none'}")
print(f"Portfolio: {result['portfolio']['action']} | Treasury: {result['treasury']}")
print("\nRANK SYMBOL       SCORE CORR RESID UP_BETA DOWN_BETA DECISION")
for rank,item in enumerate(result["ranking"],1):
    print(f"{rank:>4} {item.symbol:<11} {item.score:>5.1f} {item.correlation:>4.2f} {item.residual_correlation:>5.2f} {item.upside_beta:>7.2f} {item.downside_beta:>9.2f} {item.decision}")
