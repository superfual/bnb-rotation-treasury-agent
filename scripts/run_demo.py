import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from bnb_rotation.demo import deterministic_market
from bnb_rotation.pipeline import run_pipeline

config=json.loads((ROOT/"config/watchlist.json").read_text())
market=deterministic_market(config["candidates"]); decision=market["BTCUSDT"][-1].close_time
result=run_pipeline(market,decision,config,125,False)
print("BNB ROTATION & TREASURY CONTROL ROOM")
print("Mode: PAPER ONLY")
print("Safety: CLOSED CANDLES | NO LOOK-AHEAD | REAL ORDERS DISABLED")
print(f"Decision time: {decision} UTC-ms")
print(f"Preflight: {result['status']} | closed candles: {result.get('closed_candles_per_symbol',0)}")
print(f"BNB regime: {result.get('bnb_regime')} | portfolio: {result.get('portfolio',{}).get('action')}")
print("\nRANK  SYMBOL       SCORE  RESID  UP_BETA DOWN_BETA DECISION")
for rank,item in enumerate(result.get("ranking",[])[:8],1):
    print(f"{rank:>4}  {item.symbol:<11} {item.score:>5.1f} {item.residual_correlation:>6.2f} {item.upside_beta:>7.2f} {item.downside_beta:>9.2f} {item.decision}")
print(f"\nPaper allocations: {result.get('portfolio',{}).get('allocations',{})}")
print(f"Profit vault: {result.get('treasury')}")
