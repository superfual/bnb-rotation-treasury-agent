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

## Deployment vision
V2 may execute only qualified Spot rotations inside a separately funded Binance Agentic sub-account. It must add a strict tool allowlist, symbol-filter validation, exposure caps, idempotency, human confirmation, order reconciliation, audit evidence, and an emergency stop. This path is documented but intentionally absent from V1.

## NEXT STEP
Enable GitHub Pages from `/docs`, then record a time-bounded, read-only Binance MCP snapshot for BTCUSDT, BNBUSDT, and the candidate universe.
