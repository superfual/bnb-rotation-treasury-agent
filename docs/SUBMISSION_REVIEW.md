# Set & Earn submission review — 17 October 2026

Status: working evidence packet, not a declaration that Build is complete. This review uses retained evidence from 17 October and does not claim a fresh live-chain audit. No submission was sent, no transaction was signed, and no customer was contacted in preparing this packet.

## Identity and reviewer entry points

- Campaign wallet: `0xdcf64CdDC4a2b06F756f21a125ca393792DFA709`.
- ERC-8004 identity: #370316 on BNB Smart Chain mainnet (56).
- Registration URI: https://fual-treasury-agent.phamphuanloc.chatgpt.site/registration.json .
- Agent card: https://fual-treasury-agent.phamphuanloc.chatgpt.site/.well-known/agent-card.json .
- Public read-only A2A endpoint: https://fual-treasury-agent.phamphuanloc.chatgpt.site/a2a .
- Free customer-wallet execution beta: https://fual-treasury-agent.phamphuanloc.chatgpt.site/rebalance/ . Execution is only on BNB Smart Chain Testnet (97), with each transaction explicitly reviewed and approved by the customer.
- [Requirement-by-requirement evidence index](../evidence/testnet/CAMPAIGN_PROGRESS.md).
- [Customer beta scope and limits](CLIENT_TESTNET_BETA.md).

Current public deployment: Worker 0.1.3 / Site version 6, source `b4d0b48fadc1104ba7c1501de6f0f6ce30181043`. The A2A endpoint reads the owner's portfolio; it does not submit customer transactions. Customer execution happens in the customer's wallet browser.

## Evidence that is ready for review

| Area | Retained result | Primary evidence |
| --- | --- | --- |
| Registration | Registry ownership and registered public URI verified | [Identity](../evidence/testnet/2026-10-17-identity.json) |
| Public invocation | Browser message/send passed with matching production success log and fresh chain-97 data | [A2A result](../evidence/testnet/2026-10-17-a2a-production-success.json) |
| Three buyer hires across two marketplaces | Mandate Yield-1, HelloFugu Venus Rate Router and Mandate Guard-1 have payment evidence; HelloFugu report-call limitation remains disclosed | [Hire records](../evidence/testnet/CAMPAIGN_PROGRESS.md#hire-evidence) |
| Research commerce | Three settled research orders; actual wallet receipts total 5.88 USDC before expenses | [Sanitized orders](../evidence/testnet/2026-10-17-provider-orders.json) |
| Historical swaps | Three successful swaps on 13 October, one manual and two controller-approved | [Action inventory](../evidence/testnet/2026-10-17-action-inventory.json) |
| Identity journal | User-browser HOLD journal validated; no additional swap or execution day | [Browser check](../evidence/testnet/2026-10-17-controller-browser-journal-check.json) |
| Customer execution software | Bounded beta deployed; real customer swap still unverified | [Deployment and limits](../evidence/testnet/2026-10-17-client-beta.md) |

## Gates before claiming completion

Read-only owner execution preparation at 17 October 12:13:54 Vietnam returned
HOLD at 30.20% WBNB against a 30% target and five-percentage-point drift
threshold. Contract pins, pool identity and fresh aligned balances passed.
[Retained result](../evidence/testnet/2026-10-17-midday-execution-check.json).
No signing, broadcast, candidate swap or execution day was added. This is a
module/RPC check, not an end-to-end customer-wallet execution.

| Open item | Evidence needed to close it | Current position |
| --- | --- | --- |
| Campaign registration | Retained registration confirmation for campaign wallet | Confirmation not retained |
| Execution count and dates | At least five accepted category-consistent actions across at least three dates | Three historical candidate swaps on one date; attribution not certified |
| Qualifying independent customers | Three completed engagements for the qualifying function, with independent wallets/funding | Research settlements are real but do not prove rebalancing-service qualification |
| Marketplace/function alignment | Truthful listing and agreed scope for the actual rebalancing service | Existing research offer remains research; free beta creates no paid hire |
| Real customer execution | Voluntary customer plan, explicit approval, successful canonical receipt and exported journal | Awaiting customer test; no artificial allocation changes to create activity |
| External automated access | Organizer-compatible public invocation | Browser passed; some automated callers remain Cloudflare-1010 blocked |

Two points require organizer interpretation before stronger claims: attribution of chain-97 owner-approved controller actions to identity #370316 registered on chain 56, and whether research-only completed orders satisfy the rebalancing agent's customer criterion. Neither is assumed accepted here.

## Reproducible software check

From `public-agent/`:

```sh
node --test tests/client-engine.test.cjs tests/client-app.test.cjs tests/client-reconcile.test.cjs tests/client-routes.test.mjs tests/a2a-audit.test.mjs tests/discovery.test.mjs tests/endpoint.test.mjs
```

Re-run on 17 October: all seven test files passed, including sixteen engine checks and twelve fake-wallet UI checks. This was an offline regression check using fixtures and mocks, not a real-wallet swap, live availability probe or campaign action.

Customer exports are checked with `node scripts/verify-client-journal.cjs /absolute/path/to/export.json`. The verifier deduplicates transaction hashes, verifies receipts and reports candidate dates. HOLD, approval-only transactions, failed/pending swaps and free-page visits do not establish qualifying paid hires or rebalance execution days.

Keep private customer messages, private report URLs and signing material out of the public packet. Do not buy additional agents, fund customer wallets or generate trades merely to fill campaign counters.
