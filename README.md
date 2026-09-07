# BNB Rotation & Treasury Agent

> A defensive Binance Agent OS workflow that detects BNB-led risk-on regimes, ranks liquid Spot altcoins by stable, BTC-adjusted BNB sensitivity, and guards a BNB treasury.

**Binance Agent OS Mini Hackathon — Track A**

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
PYTHONPATH=src python -m unittest discover -s tests -v
```

Expected banner:

```text
Mode: PAPER ONLY
Safety: CLOSED CANDLES | NO LOOK-AHEAD | REAL ORDERS DISABLED
```

The deterministic demo contains candidates that merely follow BTC and candidates with measurable BNB-specific sensitivity. It proves reproducibility and defensive behavior, not profitability.

## Evidence model

The engine combines return correlation, split-window stability, BNB upside/downside beta, BTC-adjusted residual correlation, relative strength, drawdown, and liquidity. Eligibility is conjunctive: a high score cannot override a failed gate. See [methodology](docs/METHODOLOGY.md).

## Map

```text
config/watchlist.json   universe and fail-closed thresholds
src/bnb_rotation/       validation, analytics, regime, treasury
scripts/run_demo.py     deterministic control-room run
tests/                  no-look-ahead and safety regressions
docs/PROJECT_STATE.md   durable project memory
```

Educational hackathon prototype only; not financial advice.
