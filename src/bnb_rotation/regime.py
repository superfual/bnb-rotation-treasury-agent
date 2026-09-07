from statistics import fmean
from .analytics import returns

def classify_bnb_regime(bnb, btc):
    blockers=[]
    if bnb[-1].close <= fmean(c.close for c in bnb[-20:]): blockers.append("BNB_BELOW_20_SMA")
    if fmean(returns(bnb)[-10:]) <= 0: blockers.append("BNB_MOMENTUM_NOT_POSITIVE")
    if btc[-1].close <= fmean(c.close for c in btc[-50:]): blockers.append("BTC_RISK_FILTER_OFF")
    return ("RISK_ON",()) if not blockers else ("DEFENSIVE",tuple(blockers))
