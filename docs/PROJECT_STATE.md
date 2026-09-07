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
Validation/alignment, BNB regime, relationship ranking, paper allocation, profit vault, deterministic demo, walk-forward replay, benchmarks, lead/lag diagnostics, and regression tests.

## Walk-forward evidence
The replay makes each decision at close `t` and applies it only to `t → t+1`, using a rolling maximum of 120 closed candles. On the expanded Binance MCP snapshot it covered 409 periods (2025-07-24 through 2026-09-06), used a 10 bps turnover-cost approximation, and invested in 86 periods. Strategy: -13.91% return / 21.90% maximum drawdown. BNB hold: -2.30% / 58.20%. Equal-weight candidates: -49.52% / 74.00%. USDT: 0%. Drawdown protection improved, but the strategy did not beat BNB or USDT; it is not live-ready.

## Verified live snapshot
At `1788807042450` UTC-ms, Binance MCP returned 500 daily candles for all 18 symbols. Preflight found 499 aligned closed candles and admitted the latest 120 for the current decision. BNB was `RISK_ON`; only CAKEUSDT passed all relationship gates; paper portfolio was `ROTATION_READY`; treasury remained `HOLD_USDT`. Snapshot SHA-256: `263a6c59216bd8888be2eec45ec5bfa50a59f627f0d018dd407d37828822bcdb`.

## Deployment vision
V2 may execute only qualified Spot rotations inside a separately funded Binance Agentic sub-account. It must add a strict tool allowlist, symbol-filter validation, exposure caps, idempotency, human confirmation, order reconciliation, audit evidence, and an emergency stop. This path is documented but intentionally absent from V1.

## NEXT STEP
Add an explicit research viability gate and diagnose the periods responsible for underperformance before changing any thresholds. Do not enable live execution from the present evidence.
