from .analytics import relationship
from .regime import classify_bnb_regime
from .treasury import bnb_dca_decision, rotation_decision
from .validation import align_histories, closed_history

def run_pipeline(raw, decision_time, config, realized_profit_usdt=0, pullback_confirmed=False):
    required=[config["benchmark"],config["leader"],*config["candidates"]]
    missing=[s for s in required if s not in raw]
    if missing: return {"status":"BLOCKED","reason":"MISSING_SYMBOLS","missing":missing}
    history=config["history"]
    try:
        admitted={s:closed_history(raw[s],decision_time,history["minimum_closed_candles"],history["maximum_age_seconds"]) for s in required}
        aligned=align_histories(admitted)
    except ValueError as error:
        return {"status":"BLOCKED","reason":str(error)}
    btc,bnb=aligned[config["benchmark"]],aligned[config["leader"]]
    regime,blockers=classify_bnb_regime(bnb,btc)
    ranked=sorted((relationship(s,aligned[s],bnb,btc,config["ranking"]) for s in config["candidates"]),key=lambda x:x.score,reverse=True)
    return {"status":"READY","decision_time":decision_time,"closed_candles_per_symbol":len(btc),"bnb_regime":regime,"regime_blockers":blockers,"ranking":ranked,"portfolio":rotation_decision(regime,ranked,config["portfolio"]["maximum_positions"]),"treasury":bnb_dca_decision(realized_profit_usdt,regime,pullback_confirmed)}
