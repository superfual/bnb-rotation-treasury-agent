import math
from statistics import fmean
from .models import Candle, Relationship

def returns(candles):
    return [b.close / a.close - 1 for a, b in zip(candles, candles[1:])]

def _cov(a, b):
    ma, mb = fmean(a), fmean(b)
    return fmean((x-ma)*(y-mb) for x, y in zip(a, b))

def correlation(a, b):
    if len(a) != len(b) or len(a) < 2: return 0.0
    denominator = math.sqrt(_cov(a,a)*_cov(b,b))
    return _cov(a,b)/denominator if denominator else 0.0

def beta(asset, factor, predicate=None):
    pairs = [(a,f) for a,f in zip(asset,factor) if predicate is None or predicate(f)]
    if len(pairs) < 2: return 0.0
    aa, ff = map(list, zip(*pairs)); variance = _cov(ff,ff)
    return _cov(aa,ff)/variance if variance else 0.0

def residuals(asset, factor):
    slope = beta(asset,factor); intercept = fmean(asset)-slope*fmean(factor)
    return [a-intercept-slope*f for a,f in zip(asset,factor)]

def max_drawdown(candles):
    peak, worst = candles[0].close, 0.0
    for candle in candles:
        peak=max(peak,candle.close); worst=max(worst,1-candle.close/peak)
    return worst

def relationship(symbol, asset, bnb, btc, limits):
    ar, br, mr = returns(asset), returns(bnb), returns(btc)
    corr=correlation(ar,br); mid=len(ar)//2
    stability=1-min(1,abs(correlation(ar[:mid],br[:mid])-correlation(ar[mid:],br[mid:]))/2)
    up=beta(ar,br,lambda x:x>0); down=beta(ar,br,lambda x:x<0)
    residual=correlation(residuals(ar,mr),residuals(br,mr))
    strength=asset[-1].close/asset[0].close-bnb[-1].close/bnb[0].close
    draw=max_drawdown(asset); liquidity=fmean(c.quote_volume for c in asset[-30:])
    score=100*(.20*max(0,min(1,corr))+.15*stability+.20*max(0,min(1,up/2))+.15*max(0,min(1,residual))+.10*max(0,min(1,(2-down)/2))+.10*max(0,min(1,.5+strength))+.10*max(0,1-draw))
    checks=((corr>=limits["minimum_correlation"],"LOW_CORRELATION"),(residual>=limits["minimum_residual_correlation"],"BTC_EXPLAINS_RELATIONSHIP"),(up>=limits["minimum_upside_beta"],"WEAK_UPSIDE_CAPTURE"),(down<=limits["maximum_downside_beta"],"EXCESS_DOWNSIDE"),(liquidity>=limits["minimum_quote_volume"],"LOW_LIQUIDITY"),(draw<=limits["maximum_drawdown"],"EXCESS_DRAWDOWN"),(score>=limits["minimum_score"],"LOW_SCORE"))
    blockers=tuple(reason for passed,reason in checks if not passed)
    return Relationship(symbol,corr,stability,up,down,residual,strength,draw,liquidity,score,"ROTATION_READY" if not blockers else "WATCH",blockers)
