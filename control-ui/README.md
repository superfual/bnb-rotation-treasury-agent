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
the owner completed exact approvals and two swaps in Binance Wallet on 13 October 2026, then reported HOLD. See ../evidence/testnet/README.md.

The live domain is private control UI, not a public agent card or A2A endpoint.
Existing ERC-8004 identity 370316 is on chain 56. Testnet owner swaps have not
been attributed to it or confirmed as qualifying Set & Earn activity.

The connect button requests wallet_switchEthereumChain for chain 97 and only adds the fixed testnet if the wallet returns unknown-chain (4902). Rejection or unsupported switching prevents signing. Eight UI mock checks plus sixteen engine checks pass.
