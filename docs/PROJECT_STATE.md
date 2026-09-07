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
The replay makes each decision at close `t` and applies it only to `t → t+1`. On the verified Binance MCP snapshot it covered 29 periods (2026-08-08 through 2026-09-06), used a 10 bps entry-cost approximation, and invested in only 3 periods. Strategy: +2.15% return / 0.49% maximum drawdown. BNB hold: +25.36% / 4.05%. Equal-weight candidates: +47.22% / 7.76%. USDT: 0%. This is a short chronology and defense validation, not a profitability claim.

## Verified live snapshot
At `1788807042450` UTC-ms, Binance MCP returned 120 daily candles for all 18 symbols. Preflight admitted 119 aligned closed candles. BNB was `RISK_ON`; only CAKEUSDT passed all relationship gates; paper portfolio was `ROTATION_READY`; treasury remained `HOLD_USDT`. Snapshot SHA-256: `92d4eeb4d38ef48085129320be531a995aa043f23a5914109034a743c58ed351`.

## Deployment vision
V2 may execute only qualified Spot rotations inside a separately funded Binance Agentic sub-account. It must add a strict tool allowlist, symbol-filter validation, exposure caps, idempotency, human confirmation, order reconciliation, audit evidence, and an emergency stop. This path is documented but intentionally absent from V1.

## NEXT STEP
Expand the Binance MCP history beyond 120 daily candles for a longer multi-regime replay, then prepare the Track A submission video.
