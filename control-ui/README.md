# Fual Treasury control

Owner-private static Site for BNB Smart Chain Testnet 97. No backend signer,
session key, private key, credential, or real-money operation is included.

The browser engine reads aligned public RPC state, checks chain, code pins,
factory/pair/token order and reserve ratios, and produces one bounded exact
approval or swap. The owner invokes signing explicitly in an injected
EIP-1193 wallet. Limits: one U of test notional per transaction, 0.5% slippage,
1% combined fee/impact, 0.0001 tBNB gas cap, 300-second generated validity.
Nothing is scheduled or sent when the page is closed.

Immediately before the wallet request, recheck current code, allocation,
allowance, quote floor, gas, account and chain. The reviewed minimum output
and original deadline remain bound to the exact calldata. Missing allowance
produces only an exact approval (or zero reset), never a queued swap.

Receipt checking requires the exact call, success, canonical block, three
confirmations, reviewed deadline, gas cap and actual Transfer amounts for
swaps. Approvals remain separate. Cross-tab navigator locks and a persistent
pending marker prevent known duplicate requests; if the wallet returns an
ambiguous error, the owner must check wallet history before clearing it.
No aggregate daily spend authorization or autonomous signing is claimed.

Run `node tests/engine.test.cjs` and syntax checks for `dist/engine.js` and
`dist/app.js`. Test contract bytecode was captured from public testnet RPC and
checked against retained SHA-256 pins. Mock RPC tests perform no signing.
Managed preview/browser QA is skipped because control-browser is unavailable;
a real Binance Wallet end-to-end test of this Site still needs the owner.

The live domain is private control UI, not a public agent card or A2A endpoint.
Existing ERC-8004 identity 370316 is on chain 56. Testnet owner swaps have not
been attributed to it or confirmed as qualifying Set & Earn activity.

## Identity-linked owner execution journal (17 October 2026)

Before preparing a plan and again before opening a transaction, evidence.js reads ERC-8004 ownerOf(370316) and tokenURI from one fresh chain-56 block. Both must match the fixed owner and public registration URI. This is a read-only mainnet call; transactions remain testnet-97 only. An ownership/URI change, stale head or unavailable identity RPC prevents opening the transaction.

Each decision, actual pre-sign plan, broadcast hash and verified receipt is recorded locally. The plan digest binds identity observation, fixed policy and exact transaction. Journal entries form a SHA-256 hash chain to detect accidental alteration; this is NOT a wallet signature, independent registry attestation or organizer acceptance. Existing historical trades are not retroactively marked identity-bound. Pending requests retain the reviewed plan and proof; receipt verification saves its journal entry before clearing pending state. Legacy pending records are marked unbound.

Export JSON before changing browsers or clearing storage. The journal exists only in this browser, is not a remote backup, and a determined local editor can recompute hashes. Storage failure blocks a new wallet request; post-receipt storage failure leaves pending state for recovery. No unattended signing, aggregate daily budget enforcement, private key or new spending authority is added.

Tests: evidence.test.cjs covers identity, URI and stale data rejection, plan alteration, journal corruption, deduplication and storage errors. app.test.cjs includes fail-closed identity/storage and receipt-save ordering; engine limits are unchanged.
