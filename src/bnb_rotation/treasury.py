def rotation_decision(regime, ranked, maximum_positions):
    if regime != "RISK_ON": return {"action":"HOLD_USDT","allocations":{}}
    qualified=[x for x in ranked if x.decision=="ROTATION_READY"][:maximum_positions]
    if not qualified: return {"action":"NO_ACTION","allocations":{}}
    weight=round(min(.20,.80/len(qualified)),4)
    return {"action":"ROTATION_READY","allocations":{x.symbol:weight for x in qualified}}

def bnb_dca_decision(profit, regime, pullback_confirmed):
    return "BNB_DCA_READY" if profit>0 and regime=="RISK_ON" and pullback_confirmed else "HOLD_USDT"
