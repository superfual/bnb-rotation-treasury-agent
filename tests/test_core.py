import copy,json,unittest
from pathlib import Path
from bnb_rotation.analytics import correlation,residuals
from bnb_rotation.binance import candle_from_binance
from bnb_rotation.demo import DAY,deterministic_market
from bnb_rotation.pipeline import run_pipeline
from bnb_rotation.replay import lead_lag_profile,walk_forward_replay
from bnb_rotation.treasury import bnb_dca_decision
from bnb_rotation.validation import DataValidationError,closed_history
ROOT=Path(__file__).resolve().parents[1]

class CoreTests(unittest.TestCase):
    def setUp(self):
        self.config=json.loads((ROOT/"config/watchlist.json").read_text()); self.market=deterministic_market(self.config["candidates"]); self.decision=self.market["BTCUSDT"][-1].close_time
    def test_future_candle_removed(self):
        candles=self.market["BTCUSDT"]; self.assertEqual(len(closed_history(candles,candles[-2].close_time,90,172800)),119)
    def test_insufficient_fails(self):
        with self.assertRaises(DataValidationError): closed_history(self.market["BTCUSDT"][:20],self.decision,90,172800)
    def test_statistics(self):
        self.assertAlmostEqual(correlation([1,2,3],[2,4,6]),1); self.assertTrue(all(abs(x)<1e-12 for x in residuals([2,4,6,8],[1,2,3,4])))
    def test_deterministic(self):
        self.assertEqual(run_pipeline(self.market,self.decision,self.config),run_pipeline(copy.deepcopy(self.market),self.decision,self.config))
    def test_missing_symbol_blocks(self):
        del self.market[self.config["candidates"][0]]; self.assertEqual(run_pipeline(self.market,self.decision,self.config)["status"],"BLOCKED")
    def test_future_mutation_no_lookahead(self):
        baseline=run_pipeline(self.market,self.decision,self.config); future=copy.deepcopy(self.market)
        for candles in future.values():
            c=copy.copy(candles[-1]); object.__setattr__(c,"open_time",self.decision+1); object.__setattr__(c,"close_time",self.decision+DAY); object.__setattr__(c,"close",c.close*20); candles.append(c)
        self.assertEqual(baseline,run_pipeline(future,self.decision,self.config))
    def test_profit_does_not_force_dca(self):
        self.assertEqual(bnb_dca_decision(100,"RISK_ON",False),"HOLD_USDT")
    def test_binance_kline_mapping(self):
        row=[1000,"1","2","0.5","1.5","10",1999,"15",3,"4","6","0"]
        candle=candle_from_binance(row)
        self.assertEqual((candle.open_time,candle.close_time,candle.close,candle.quote_volume),(1000,1999,1.5,15.0))
    def test_walk_forward_uses_next_period_only(self):
        market=deterministic_market(self.config["candidates"],count=130)
        times=[c.close_time for c in market["BTCUSDT"]][89:]
        baseline=walk_forward_replay(market,times,self.config)
        changed=copy.deepcopy(market)
        future_time=times[-1]
        for candles in changed.values():
            candle=candles[-1]
            if candle.close_time==future_time:
                object.__setattr__(candle,"close",candle.close*10)
        earlier=walk_forward_replay(changed,times[:-1],self.config)
        self.assertEqual(baseline["records"][:-1],earlier["records"])
    def test_walk_forward_is_deterministic_and_has_benchmarks(self):
        market=deterministic_market(self.config["candidates"],count=130)
        times=[c.close_time for c in market["BTCUSDT"]][89:]
        first=walk_forward_replay(market,times,self.config,fee_rate=.001)
        second=walk_forward_replay(copy.deepcopy(market),times,self.config,fee_rate=.001)
        self.assertEqual(first,second)
        self.assertEqual(set(first["benchmarks"]),{"bnb_hold","equal_weight_candidates","usdt_hold"})
        self.assertEqual(first["periods"],40)
    def test_lead_lag_alignment(self):
        market=deterministic_market(self.config["candidates"],count=120)
        profile=lead_lag_profile(market["ETHUSDT"],market["BNBUSDT"],3)
        self.assertEqual(set(profile),{"0","1","2","3"})

if __name__=="__main__": unittest.main()
