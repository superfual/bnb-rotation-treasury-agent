# Customer-wallet treasury rebalancing beta

Public entry: https://fual-treasury-agent.phamphuanloc.chatgpt.site/rebalance/

Same agent identity: ERC-8004 #370316 on chain 56. Execution is exclusively BNB Smart Chain Testnet 97. This is an unpaid self-service beta, not a marketplace order, completed hire, production mainnet strategy or guaranteed return.

## What the customer receives

The browser reads the customer's own connected wallet and proposes a fixed 30% test WBNB / 70% test U allocation when drift reaches five percentage points. One transaction is capped at one test U of notional. Contract/code pins, the fixed PancakeSwap router/pair, a 0.5% slippage floor, 1% fee/impact limit, 300-second plan life and 0.0001 tBNB gas cap are unchanged from the owner experiment. Exact approvals are separate from swaps.

The customer retains custody and explicitly confirms each transaction. The application never requests a seed phrase or private key; it does not grant a session, accept principal into an agent wallet, trade unattended or charge a management fee. Gas is paid from the customer's testnet wallet.

## Customer flow

1. Open the public entry in a compatible injected wallet browser (including Binance Wallet Discover) and connect the customer's own wallet. The page requests chain 97 and refuses if switching is rejected.
2. Choose 'Kiểm tra & lập kế hoạch'. Identity #370316 is checked on chain 56; portfolio/contracts are checked on chain 97. Empty or in-band portfolios may return HOLD and send no transaction.
3. If an adjustment is needed, review its exact amount, recipient, output floor and fee. Approve only the displayed testnet call. The page reconciles receipts and actual token transfers, then prepares a fresh decision on request. No forced trade is needed for an in-band portfolio.
4. Export the JSON journal before switching browsers or deleting site storage. It binds plans and verified receipt hashes to the observed identity and fixed policy. It is local data, not a signature or an independently certified registry attestation.

Only the fixed test U (`0xc70b8741b8b07a6d61e54fd4b20f22fa648e5565`) and test WBNB (`0xae13d989dac2f0debff460ac112a837c89baa7cd`) on chain 97 are used. Test pool reserve pricing is not USD pricing. Mainnet assets are unsupported by this beta.

## Verification and day accounting

From `public-agent/`, run:

```sh
node scripts/verify-client-journal.cjs /absolute/path/to/export.json
```

The verifier checks the journal chain, original plan digests, pinned execution policy, sign-plan/confirmation order and canonical chain-97 receipts via the existing receipt verifier. It deduplicates transaction hashes and reports swap dates in UTC and Vietnam time. HOLD, approvals, pending/reverted receipts and transactions outside the campaign window are not added to its candidate swap counter. Candidate counts are not organizer acceptance.

## Commercial and campaign gates

Do not sell autonomous mainnet management using this beta. Existing TermiX research orders keep their historical research scope. A new paid engagement requires a genuine customer need, agreed execution scope and deliverable, and a working validated flow; using this free page alone is not a paid hire event. Client funding independence must be documented separately. The builder must not fund customer wallets or use circular activity to manufacture usage.

TermiX's current public configuration does expose Quant on chain 56. That is a different, mainnet session-based product. No key was registered, application submitted, fee terms accepted, session granted or client funds requested in this work. Mainnet readiness remains unresolved. See `evidence/testnet/2026-10-17-termix-quant-readiness.json`.

Validation: sixteen complete engine checks run with a non-owner customer address; twelve fake-wallet UI flow checks include switching accounts after review, identity failure and storage failure. Asset-route/content/CSP tests, unchanged A2A tests and reconciliation tests pass. Managed visual QA and a real customer-wallet swap remain unverified; no new transaction was sent during implementation.
