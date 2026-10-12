# Owner-reviewed testnet treasury rebalancing

This adds a real EVM transaction construction/simulation path, not a claim of
live deployment. The research strategy remains `FAILED_NOT_LIVE_READY` and
mainnet execution remains absent. The new experiment has a different input:
an owner-approved two-token target allocation on BSC testnet, not automatic
alpha decisions from the failed research strategy.

## Implemented

- `onchain.py`: chain-97-only policy, exact decimal token amounts, live code
  pins, aligned block reads, token balance/decimals/allowance, direct V2 quotes,
  target drift, per-trade test notional, quote-impact/slippage limits and gas
  cap. No transfers, native swaps, bridges, leverage or key loading.
- `plan_testnet_rebalance.py`: builds one simulated unsigned transaction.
  No signing/broadcast method exists in its RPC allowlist.
- An insufficient allowance produces only a zero-reset/exact approval. A
  receipt and fresh plan are required before a swap; the initial swap is never
  presented as simulated when approval is still missing.
- `testnet-wallet-review.html`: keyless EIP-1193 signing in the owner's browser.
  Rechecks chain, wallet, code, quote, balance, target direction, calldata,
  amount, slippage, expiry and gas. One explicit wallet signature per action.
- `verify_testnet_receipt.py`: matches real transaction sender/to/input/value,
  receipt success and canonical block, expiry and actual gas to the reviewed
  plan. Distinguishes approval from DEX swap. No inferred campaign qualification.

## Configure before use

Copy `config/testnet-rebalance.example.json` into ignored `execution-local/`.
The placeholders deliberately fail validation. An operator must verify the
router and both token contracts, inspect liquidity, and pin each runtime
bytecode SHA-256. A bytecode pin proves consistency, not correctness or an
audit; proxy upgrades/behavior are not generally captured by a runtime pin.
Use only verified standard non-fee-on-transfer ERC-20 test tokens and a liquid
direct two-token pair. Unsupported decimals (>18), empty pools or unavailable
RPC reads block the plan. Native tBNB is reserved for gas, not allocated.

PancakeSwap's primary docs list the chain-97 V2 router as
`0xD99D1c33F9fC3444f8101754aBC46c52416550D1` and factory as
`0x6725F303b657a9451d8BA641348b6761A6CC7a17`.
Do not assume any arbitrary test stablecoin has a pool on that router.
The example contains no preapproved token/pair or fabricated liquidity.
`config/testnet-rebalance.verified.json` records a separate live-read candidate:
the official router, Altana test $U
`0xc70B8741B8B07A6d61E54fd4B20f22Fa648E5565`, and WBNB returned by the router
`0xae13d989dac2f0debff460ac112a837c89baa7cd`.
On 13 October 2026 UTC+7 a read of the actual pool returned
`1 test U -> 0.005040429466318224 WBNB`. This is a historical quote, not a
current executable price or proof that the pool is safe. Runtime bytecode pins
were collected from chain 97; independent source/implementation review remains
required. Test $U is not USDC, USDT or real dollars. No funds were sent.

```bash
python scripts/plan_testnet_rebalance.py \
  --policy execution-local/policy.json \
  --rpc https://bsc-testnet-dataseed.bnbchain.org \
  --output execution-local/new-plan.json
```

Default example: 30% asset target / 70% settlement, 5 percentage-point drift,
1 test settlement unit per trade, 0.5% slippage, 1% quote impact, 0.0001 tBNB
gas cap, 180-second validity. These are experiment settings, not a funded or
approved production investment policy. Token settlement units are not USD.

Host the review page over HTTPS (or localhost on desktop), open it inside the
owner's wallet browser and load the fresh plan. WebCrypto requires a secure
context. It does not connect automatically, request a private key or switch
to mainnet. After clicking the button, inspect the wallet's own transaction
simulation before signing. If the wallet/browser lacks the required read/RPC
methods, stop; never bypass a failed simulation.

After signing, record the actual transaction:

```bash
python scripts/verify_testnet_receipt.py \
  --plan execution-local/new-plan.json --tx-hash ACTUAL_TX_HASH \
  --rpc https://bsc-testnet-dataseed.bnbchain.org \
  --output execution-local/receipt-ACTUAL_TX_HASH.json
```

Broadcast is not success. A reverted or pending transaction does not generate
evidence. A successful router call is not a verified portfolio result: inspect
actual output/transfer logs and post-swap balances independently. Reconciliation
of amounts, fee-on-transfer behavior and multi-block finality are not implemented.
Private local receipt files are not a public campaign evidence index.

## Remaining deployment boundaries

No testnet transaction, session grant, liquidity deployment, contract funding or
hosting was performed by this change. There is no unattended runner, durable
wallet session or daily spend ledger. Repeated owner-approved plans each respect
a per-trade cap; they do not implement an aggregate daily authorization.
The browser page has syntax/unit checks, not a real Binance keyless wallet
end-to-end test. Concurrent signing from multiple tabs is not coordinated.

The existing identity remains agent `370316` on chain `56` owned by the
campaign wallet. Do not remint the same agent on chain 97 or claim testnet swaps
from the owner wallet automatically belong to that mainnet identity. Campaign
attribution, identity/card domain, live invocation and marketplace execution
listing must be resolved before claiming qualifying activity. Existing research
orders are real paid reports, not proof that this execution experiment is hired.
Never force trades or change targets to manufacture five transactions.

## Verification and sources

Run `PYTHONPATH=src python -m unittest discover -s tests -v`.
Run `node tests/test_wallet_review.cjs` for four fake-provider checks of the
keyless review page (valid approval, wrong chain, changed plan and expiry).
Tests exercise real encodings against fixtures: exact approval, sell/buy/hold,
bounded policies, stale/wrong-chain reads, reverts, code/price/gas failures and
foreign/failed receipts. Fixtures are not chain executions.

- https://developer.pancakeswap.finance/contracts/v2/addresses
- https://developer.pancakeswap.finance/contracts/v2/router-v2
- https://docs.altana.network/sdk/bnb-testnet
- https://docs.altana.network/sdk/execute

Altana sessions are a future unattended integration, not implemented here;
the owner wallet remains the only signing authority in this experiment.
