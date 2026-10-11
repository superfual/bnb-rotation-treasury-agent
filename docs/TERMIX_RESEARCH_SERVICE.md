# Operator-reviewed TermiX research service

The registered agent is `fual-treasury.agent`, ERC-8004 token `370316` on BSC (56).
Marketplace agent ID: `cmv272a0kg4y8zw01sg7tclan`.
Research listing ID: `cmv2uos8s0grdwx01t9j48xdi`.
Published service: BNB Ecosystem Portfolio & Treasury Research, 2 USDC, two days
after requirements and scope are agreed. Instant purchase and automatic quoting
are disabled. The operator reviews every report before delivery.

## What is connected today

TermiX cloud hosting handles the service FAQ and collects requirements from the
reviewed knowledge base. It does **not** run this Python engine. The local report
builder connects a structured intake to the existing BNB/BTC analysis pipeline,
but is not a deployed order-processing worker. These are separate capabilities.

## Input and reproducible draft generation

1. Collect the requested symbols (one to five explicit Spot USDT pairs), horizon,
   question, and optionally portfolio weights. Weights are fractions totalling
   one, including an explicit USDT reserve. Review marketplace scope first.
2. Use Binance MCP `spot.klines`, interval `1d`, UTC, limit at least 121, for
   BTCUSDT, BNBUSDT and all requested symbols. Record one collection cutoff.
   Do not acquire exchange account credentials or call trading tools.
3. Save an injected snapshot with `source: "Binance MCP Server spot.klines"`,
   `mode: "READ_ONLY"`, `market: "SPOT"`, `interval: "1d"`,
   `decision_time_utc_ms`, and a symbol-keyed `histories` map of native kline rows.
   The metadata is host-supplied provenance, not cryptographic source attestation.
4. Generate the draft within fifteen minutes of collection:

```bash
python scripts/build_service_report.py \
  --snapshot service-local/snapshot.json \
  --request config/service-request.example.json \
  --output service-local/new-report
```

The output directory must not already exist, preventing accidental overwrite.
The command emits `report.json` and `report.md`. Both are drafts, never a paid
delivery or proof of campaign qualification. Actual client intake and reports
belong in the ignored `service-local/` directory, not public git history.

The report rejects stale/future collection times, incomplete daily history,
duplicates, gaps, wrong intervals, non-finite/invalid OHLCV, and unmatched assets.
It excludes open candles and keeps exactly 120 aligned closed daily candles.

## Interpretation

The engine uses daily BNB/BTC regime filters, BNB-relative relationship metrics,
BTC-adjusted residuals, risk gates, and the existing shock filter. It reports
7/30-day returns, moving averages, historical drawdown, and Spot quote-volume
observations. Optional portfolio checks flag the configured 20% per-asset limit
and 20% USDT reserve floor; these are model settings, not universal risk limits.

The ranking only covers the requested candidate subset. Daily observations do
not establish on-chain liquidity, execution quality, contract safety, or future
returns. The historical strategy failed live-readiness gates. A current ranking
does not override that result. The question/horizon are retained for operator
interpretation; free text does not silently change model thresholds.

## Next integration boundary

Before a deployed worker can fulfill orders, it needs an agreed hosting location,
market-data adapter available in that runtime, persistent job state and
idempotency, order/funding checks, artifact upload, operator review and explicit
delivery. Enabling an external TermiX runtime can pause cloud hosting; do not
poll its runtime inbox merely to test this local report generator.

No messaging, quoting, escrow movement, wallet signing or order execution occurs
in this module. It does not implement the qualifying on-chain treasury actions
required by Set & Earn. Campaign compliance remains a separate workstream.
