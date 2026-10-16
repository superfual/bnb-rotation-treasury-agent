# Customer-wallet beta implementation

Site version 6 / Worker 0.1.3 deployed publicly from source `b4d0b48fadc1104ba7c1501de6f0f6ce30181043` at 2026-10-16T21:16:30Z (17 October 04:16:30 Vietnam). Deployment `appgdep_6ad29419842881919943493c47ac1f0c`.

URL: https://fual-treasury-agent.phamphuanloc.chatgpt.site/rebalance/

This adds an unpaid, customer-wallet, explicit-approval testnet flow under the same identity, rather than sending all visitors to the owner's fixed portfolio. It retains contract/gas/amount/drift controls and the identity-linked journal. The existing public A2A owner-status interface stays read-only. Only five fixed client assets are served; no local environment files or private controller access settings were published.

Sixteen engine checks with a non-owner wallet and twelve fake-wallet UI checks passed; public asset routing/CSP tests and existing A2A regression checks passed. Reconciliation tooling passed HOLD exclusion, duplicate hash exclusion and pending/revert/tamper/order rejection checks. The real owner HOLD export was processed as zero swaps and zero dates. Native deployment succeeded; browser visual QA and a real client-wallet swap have not yet been verified.

No paid order, key registration, mainnet application, session authority, customer message, customer funding or new transaction was created. The prior three same-day owner swaps remain unchanged. No customer hire or execution day is added by this publication. Service onboarding and limits: ../../docs/CLIENT_TESTNET_BETA.md.
