def _daily_return(candles):
    return candles[-1].close / candles[-2].close - 1


def apply_shock_filter(portfolio, bnb, btc, candidates, limits):
    allocations = dict(portfolio["allocations"])
    if not allocations:
        return portfolio, ()

    blockers = []
    if _daily_return(bnb) <= limits["leader_daily_return_floor"]:
        blockers.append("BNB_DAILY_SHOCK")
    if _daily_return(btc) <= limits["benchmark_daily_return_floor"]:
        blockers.append("BTC_DAILY_SHOCK")
    latest = bnb[-1]
    close_location = (latest.close - latest.low) / (latest.high - latest.low) if latest.high > latest.low else 0.0
    if close_location < limits["minimum_leader_close_location"]:
        blockers.append("BNB_WEAK_DAILY_CLOSE")
    if blockers:
        return {"action": "HOLD_USDT", "allocations": {}}, tuple(blockers)

    admitted = {}
    for symbol, weight in allocations.items():
        if _daily_return(candidates[symbol]) >= limits["candidate_daily_return_ceiling"]:
            blockers.append(f"{symbol}_EXTENSION")
        else:
            admitted[symbol] = weight
    action = "ROTATION_READY" if admitted else "HOLD_USDT"
    return {"action": action, "allocations": admitted}, tuple(blockers)
