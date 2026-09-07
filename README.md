# BNB Rotation & Treasury Agent

> A defensive Binance Agent OS workflow that detects BNB-led risk-on regimes, ranks liquid Spot altcoins by stable, BTC-adjusted BNB sensitivity, and guards a BNB treasury.

**Binance Agent OS Mini Hackathon — Track A**

**[Open the BNB Rotation Control Room](https://superfual.github.io/bnb-rotation-treasury-agent/)**

## Safety boundary

- PAPER ONLY; no exchange-order path exists.
- Binance Spot data is host-injected through MCP.
- Only candles closed by one UTC decision time are admitted.
- Missing, stale, unordered, future, or insufficient data fails closed.
- A ranking never grants permission to trade.
- Profit never forces a BNB purchase.

## Thesis

Raw BNB correlation can be misleading when both assets merely follow Bitcoin. The agent therefore asks which liquid Spot assets repeatedly capture more BNB upside without unacceptable downside **after removing their linear BTC exposure**.

```text
Binance MCP → Closed-candle preflight → BTC filter → BNB regime
→ Relationship metrics → BTC residuals → Risk gates → Ranking
→ Paper rotation → USDT profit vault → Independent BNB DCA guard
```

Outputs: `ROTATION_READY`, `WATCH`, `HOLD_USDT`, `ROTATE_OUT`, `BNB_DCA_READY`, `NO_ACTION`.

## Reproduce

Python 3.11+, no runtime dependencies or credentials:

```bash
python scripts/run_demo.py
python scripts/run_replay.py
PYTHONPATH=src python -m unittest discover -s tests -v
```

Expected banner:

```text
Mode: PAPER ONLY
Safety: CLOSED CANDLES | NO LOOK-AHEAD | REAL ORDERS DISABLED
```

The deterministic demo contains candidates that merely follow BTC and candidates with measurable BNB-specific sensitivity. It proves reproducibility and defensive behavior, not profitability.

## Walk-forward replay

The replay freezes information at each daily close and applies the resulting paper allocation only to the next close-to-close period. It reports the strategy beside BNB hold, equal-weight candidates, and USDT, and records BNB-to-alt lead/lag correlations separately without claiming causality.

The expanded Binance MCP snapshot provides 409 out-of-sample periods from 2025-07-24 through 2026-09-06. With a rolling 120-candle analysis window and 10 bps turnover-cost approximation, the strategy returned -13.91% with 21.90% maximum drawdown and invested in 86 periods. BNB hold returned -2.30% with 58.20% drawdown; equal-weight candidates returned -49.52% with 74.00% drawdown; USDT was flat. The agent reduced drawdown materially but failed to outperform BNB and USDT. Therefore the research gate is **NOT LIVE READY**. The gate is implemented in code and cannot be overridden by a current candidate ranking. See the [loss attribution and research diagnostics](docs/RESEARCH_DIAGNOSTICS.md).

## Verified Binance MCP snapshot

A time-bounded read-only snapshot at decision time `1788807042450` UTC-ms requested 500 daily candles for all 18 symbols. The current daily candle was excluded, leaving 499 aligned closed candles; each decision uses at most the latest 120. Result: BNB `RISK_ON`; CAKEUSDT was the only current candidate to pass every configured gate; paper portfolio `ROTATION_READY`; BNB profit vault `HOLD_USDT`. Snapshot SHA-256: `263a6c59216bd8888be2eec45ec5bfa50a59f627f0d018dd407d37828822bcdb`.

The committed evidence summary records the input hash and complete ranking. Raw market rows are intentionally not served by the public dashboard. No account or trading tool was called during acquisition.

## Evidence model

The engine combines return correlation, split-window stability, BNB upside/downside beta, BTC-adjusted residual correlation, relative strength, drawdown, and liquidity. Eligibility is conjunctive: a high score cannot override a failed gate. See [methodology](docs/METHODOLOGY.md).

## Map

```text
config/watchlist.json   universe and fail-closed thresholds
src/bnb_rotation/       validation, analytics, regime, treasury
scripts/run_demo.py     deterministic control-room run
scripts/run_replay.py   deterministic walk-forward replay
tests/                  no-look-ahead and safety regressions
docs/PROJECT_STATE.md   durable project memory
```

Educational hackathon prototype only; not financial advice.

## Guarded live-execution vision

V1 stops at deterministic paper decisions. Its next safe deployment target is a dedicated Binance Agentic sub-account—not a master account—with a Spot-only tool allowlist, capped exposure, idempotent client order IDs, an explicit human confirmation step, post-trade reconciliation, and an emergency stop. Margin, Futures, Convert, withdrawal, and cross-wallet transfer remain denied.

This is an architectural extension, not a claim that V1 submits orders. See the [guarded execution roadmap](docs/LIVE_EXECUTION_ROADMAP.md).
