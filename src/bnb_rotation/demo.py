import math, random
from .models import Candle
DAY=86_400_000

def deterministic_market(symbols,count=120,start=1_700_000_000_000):
    rng=random.Random(71)
    btc=[.002+.008*math.sin(i/7)+rng.uniform(-.004,.004) for i in range(count)]
    alpha=[.001+.006*math.sin(i/5) for i in range(count)]
    bnb=[.65*m+a for m,a in zip(btc,alpha)]
    def make(series,price,liquidity):
        result=[]
        for i,change in enumerate(series):
            opened=price; price=max(.01,price*(1+change)); t=start+i*DAY
            result.append(Candle(t,t+DAY-1,opened,max(opened,price)*1.003,min(opened,price)*.997,price,liquidity/price,liquidity))
        return result
    market={"BTCUSDT":make(btc,50000,2e9),"BNBUSDT":make(bnb,500,2.5e8)}
    for i,symbol in enumerate(symbols):
        sensitivity=1.35 if i<4 else .35
        series=[.70*m+sensitivity*a+rng.uniform(-.005,.005) for m,a in zip(btc,alpha)]
        market[symbol]=make(series,10+i,4e7-i*5e5)
    return market
