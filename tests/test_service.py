import copy
import json
import unittest
from pathlib import Path

from bnb_rotation.demo import deterministic_market
from bnb_rotation.service import DAY, SOURCE, build_report, render_markdown

ROOT = Path(__file__).resolve().parents[1]


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((ROOT / "config/watchlist.json").read_text())
        market = deterministic_market(["CAKEUSDT"], count=121)
        # Use real UTC daily boundary semantics independent of the demo fixture.
        histories = {}
        for symbol, candles in market.items():
            histories[symbol] = [[i * DAY, c.open, c.high, c.low, c.close, c.volume,
                                   (i + 1) * DAY - 1, c.quote_volume, 0, 0, 0, 0]
                                  for i, c in enumerate(candles)]
        self.now = 120 * DAY + 12_345
        self.snapshot = {"source": SOURCE, "mode": "READ_ONLY", "market": "SPOT",
                         "interval": "1d", "decision_time_utc_ms": self.now, "histories": histories}
        self.request = {"request_id": "TEST-001", "symbols": ["CAKEUSDT"],
                        "time_horizon": "one month", "question": "Compare CAKE with BNB.",
                        "weights": {"CAKEUSDT": .8, "USDT": .2}}

    def run_report(self):
        return build_report(self.snapshot, self.request, self.config, self.now)

    def test_draft_flags_concentration_and_does_not_claim_execution(self):
        report = self.run_report()
        self.assertEqual(report["status"], "DRAFT_REQUIRES_OPERATOR_REVIEW")
        self.assertEqual(report["analysis"]["portfolio_risk"]["above_configured_weight_limit"], {"CAKEUSDT": .8})
        self.assertEqual(report["data"]["candles_per_symbol"], 120)
        self.assertIn("Operator review required", render_markdown(report))

    def test_unclosed_extreme_price_cannot_change_analysis(self):
        baseline = self.run_report()
        for rows in self.snapshot["histories"].values():
            rows[-1][4] = 1e100
        self.assertEqual(baseline["analysis"], self.run_report()["analysis"])

    def test_missing_internal_day_blocks_even_with_enough_rows(self):
        rows = self.snapshot["histories"]["CAKEUSDT"]
        rows[50][0] += DAY
        with self.assertRaisesRegex(ValueError, "missing daily candles"):
            self.run_report()

    def test_stale_latest_close_blocks(self):
        for rows in self.snapshot["histories"].values():
            for row in rows:
                row[0] -= 2 * DAY
                row[6] -= 2 * DAY
        with self.assertRaisesRegex(ValueError, "stale latest"):
            self.run_report()

    def test_invalid_ohlcv_and_nan_block(self):
        for value in (-1, float("nan")):
            with self.subTest(value=value):
                original = self.snapshot["histories"]["CAKEUSDT"][50][4]
                self.snapshot["histories"]["CAKEUSDT"][50][4] = value
                with self.assertRaises(ValueError):
                    self.run_report()
                self.snapshot["histories"]["CAKEUSDT"][50][4] = original

    def test_snapshot_time_cannot_be_future_or_reused_after_fifteen_minutes(self):
        for now in (self.now - 1, self.now + 900_001):
            with self.assertRaisesRegex(ValueError, "collection time"):
                build_report(self.snapshot, self.request, self.config, now)

    def test_missing_symbol_and_futures_source_block(self):
        del self.snapshot["histories"]["CAKEUSDT"]
        with self.assertRaisesRegex(ValueError, "missing data"):
            self.run_report()
        self.snapshot["market"] = "FUTURES"
        with self.assertRaisesRegex(ValueError, "Spot candles"):
            self.run_report()

    def test_bad_weights_and_oversized_requests_block(self):
        for weights in ({"CAKEUSDT": .8}, {"CAKEUSDT": True}, {"CAKEUSDT": float("inf")}, {"BTCUSDT": 1}):
            with self.subTest(weights=weights):
                self.request["weights"] = weights
                with self.assertRaises(ValueError):
                    self.run_report()
        self.request.pop("weights")
        self.request["symbols"] = ["CAKEUSDT"] * 6
        with self.assertRaisesRegex(ValueError, "one to five"):
            self.run_report()

    def test_benchmark_only_request_and_absent_portfolio(self):
        self.request["symbols"] = ["BNBUSDT"]
        self.request.pop("weights")
        report = self.run_report()
        self.assertEqual(report["analysis"]["ranking"], [])
        self.assertIsNone(report["analysis"]["portfolio_risk"])
        self.assertEqual(report["analysis"]["assets"][0]["symbol"], "BNBUSDT")

    def test_report_is_deterministic_and_does_not_mutate_config(self):
        config = copy.deepcopy(self.config)
        self.assertEqual(self.run_report(), self.run_report())
        self.assertEqual(self.config, config)


if __name__ == "__main__":
    unittest.main()
