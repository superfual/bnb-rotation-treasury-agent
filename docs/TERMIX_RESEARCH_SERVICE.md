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

## Read-only order queue

`scripts/termix_research_queue.py` uses the official TermiX 1.8 skill's API
helper and the existing linked web account on BSC. It calls only REST GETs,
never the A2A inbox, so it does not take over cloud hosting. Install/update the
official skill and keep its credential working directory outside the repo.

```bash
python scripts/termix_research_queue.py \
  --skill-dir /path/to/termix-agent-skills \
  --credential-workdir /path/to/linked-account inspect
```

It paginates provider orders scoped to this agent and research listing. A
`PENDING_ACCEPT` order needs wallet acceptance, not a draft. Draft generation
requires authenticated membership, matching listing, indexed chain order and
escrow identities, `FUNDED`/`IN_PROGRESS`, a future timezone-aware delivery
deadline, and `availableActions.canSubmitDelivery: true`.

After reviewing the client's scope, write a private intake file:

```json
{
  "order_id": "ACTUAL_ORDER_ID",
  "scope_reviewed": true,
  "request": {
    "request_id": "ACTUAL_ORDER_ID",
    "symbols": ["CAKEUSDT"],
    "time_horizon": "one month",
    "question": "Client's agreed research question"
  }
}
```

Then run the same command with `draft --intake service-local/intake.json
--snapshot service-local/snapshot.json`. The snapshot must still be fresh.
The queue rechecks order membership and state after calculation and atomically
saves a report plus a hash manifest in `service-local/queue/<order-id>/`.
A lock prevents concurrent duplicate work. Retries verify hashes and reuse the
existing draft; changed intake/config/order state (including redo) or modified
artifacts require operator review. Do not delete a stale lock until checking
that its worker has stopped. A hard process crash can leave a lock or temporary
directory; no unattended cleanup is performed.

No free-text message is treated as an agreed intake. No report is uploaded or
submitted, and no provider acceptance is signed. Before later delivery, the
operator must review the draft and recheck the live order/deadline. These are
manual commands, not a deployed continuous worker. Unit fixtures demonstrate
state handling, not real on-chain orders or completed hires.

## Review and delivery handoff

The queue CLI also supports `review`, `approve` and `prepare-delivery`, with
the same `--skill-dir` and `--credential-workdir` arguments. None of these
commands uploads a file, prepares a real transaction, signs or submits a
delivery. The actual API steps below remain an operator-driven workflow.

1. Run `review --order ACTUAL_ORDER_ID`. It checks the live order and original
   artifact hashes, then creates `review/report.md`. Inspect and, if needed,
   edit this client-facing copy. Re-running review preserves your edits.
   The copied draft retains its labels and limitations until the operator
   revises them; this command does not imply approval or complete the client's
   requested interpretation.
2. Review the final exact file bytes. Only after the human approves that
   version, run `approve --order ACTUAL_ORDER_ID --report-sha256 FINAL_HASH
   --reviewer "Operator name" --note "What was checked"`. The hash is an
   acknowledgement of the exact content reviewed, not evidence that a human
   approved it unless the command follows their explicit instruction. Never
   approve a real client report solely because its generator/tests passed.
3. Run `prepare-delivery --order ACTUAL_ORDER_ID`. It verifies approval binds
   the source manifest, report bytes and unchanged live order. It emits
   `delivery-plan.json`, including the approved Markdown file, checksum,
   upload/register request shapes and final transaction handoff. Editing the
   approved report invalidates approval. A new approval clears the old plan.

The plan is a local recipe with response placeholders, not an unsigned
transaction returned by TermiX. Always rerun preparation immediately before
starting upload, and re-read the order/deadline immediately before submission.
Old plan files are not authorization to upload or sign. Original private
`report.json`, manifest, approval notes and client intake are not deliverables;
only the approved client-facing Markdown copy is selected for upload.

For an approved real order, use the documented official skill workflow:

- `POST /api/v1/orders/:id/delivery/upload-url` with the plan's file metadata;
  PUT exactly the approved bytes to the returned presigned URL.
- Verify the uploaded checksum and register its actual `s3Key`/`publicUrl`
  through `POST /api/v1/orders/:id/delivery/artifacts`.
- Recheck the live order. Use the returned real artifact ID in
  `POST /api/v1/orders/:id/delivery/submit`, which returns a tx-intent.
- `validate_delivery_intent` checks the envelope action, BSC chain, escrow
  contract, calldata format and zero native value. It does not decode calldata
  or replace wallet simulation/review. Verify the actual order/artifact binding
  and use the official transaction helper for web-wallet signing.
- Wait for the indexer to show `DELIVERED`. A plan, upload, API intent or
  transaction broadcast is not proof of indexed delivery or payment.

Source: official TermiX 1.8 `docs/provider-order-delivery.md` and
[Orders API reference](https://docs.termix.ai/api-reference/orders).
No self-hire or mock order is represented as campaign evidence.

## Next integration boundary

Before a deployed worker can fulfill orders, it needs an agreed hosting location,
market-data adapter available in that runtime, durable queue storage,
artifact upload, operator review and explicit
delivery. Enabling an external TermiX runtime can pause cloud hosting; do not
poll its runtime inbox merely to test this local report generator.

No messaging, quoting, escrow movement, wallet signing or order execution occurs
in this module. It does not implement the qualifying on-chain treasury actions
required by Set & Earn. Campaign compliance remains a separate workstream.
