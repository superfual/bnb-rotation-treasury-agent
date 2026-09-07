# Project State

## Product
BNB Rotation & Treasury Agent — Binance Agent OS Mini Hackathon Track A.

## Invariants
- PAPER ONLY; no order adapter.
- Closed candles, one decision time, no look-ahead.
- Bad or insufficient history fails closed.
- BTC-adjusted evidence is mandatory.
- Rotation requires BNB `RISK_ON` and every candidate gate.
- Profit stays in USDT unless the separate BNB DCA guard passes.

## Implemented
Validation/alignment, BNB regime, relationship ranking, paper allocation, profit vault, deterministic demo, and regression tests.

## NEXT STEP
Verify CI on `main`, then add a judge-facing GitHub Pages dashboard and a host-injected Binance MCP snapshot.
