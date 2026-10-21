# Set & Earn submission review — 21 October 2026

Current evidence: [requirement matrix and remaining gaps](../evidence/testnet/CAMPAIGN_PROGRESS.md).

Campaign wallet `0xdcf64cddc4a2b06f756f21a125ca393792dfa709`; ERC-8004 **#370316, chain 56**, execution chain **97**. Public repository: https://github.com/superfual/bnb-rotation-treasury-agent .

## Ready for review

- Four distinct buyer-hire records across Mandate, HelloFugu and Pokter. Three agents/two marketplaces are covered numerically; provider-call/delivery limitations remain disclosed.
- Five SETTLED customer orders, preserving actual research, partial-support and HOLD scopes. Independent funding/control remains unconfirmed. The completed-hire rule is not rewritten to require a swap in every order.
- Five successful candidate swaps on three dates, **13, 20 and 21 October**: [inventory](../evidence/testnet/2026-10-21-action-inventory.json). Approvals, wraps and commerce transactions are excluded.
- Fresh ERC-8004 owner/URI check: [identity](../evidence/testnet/2026-10-21-identity.json).
- Public owner-approved Testnet rebalancing-support listing under the same agent identity. Historical research work is not relabeled.

## Gaps still open

| Item | Outcome of this audit |
| --- | --- |
| Agent execution attribution | Receipt reconciliation passed; original 20/21 October signing journals absent. One 13 October swap manual; no autonomous signer. Chain-56 identity / chain-97 activity requires review. [Audit](../evidence/testnet/2026-10-21-attribution-audit.md) |
| Current external access | Card, registration URI and POST /a2a returned Cloudflare 403/1010 in normal automated checks. Historical 17 October browser success is retained. No fix or bypass claimed |
| Campaign registration | Owner previously reported form filled; original confirmation and submitted-wallet record not recovered. [Registration review](../evidence/testnet/2026-10-21-registration-review.md) |
| Customer independence | Five distinct buyer wallets retained; distinctness does not prove independent control or funding |

## Reviewer entry points

- Registered URI: https://fual-treasury-agent.phamphuanloc.chatgpt.site/registration.json
- Card: https://fual-treasury-agent.phamphuanloc.chatgpt.site/.well-known/agent-card.json
- Public read-only A2A: https://fual-treasury-agent.phamphuanloc.chatgpt.site/a2a
- Customer-wallet beta: https://fual-treasury-agent.phamphuanloc.chatgpt.site/rebalance/
- Paid service: https://www.agent.family/listing?id=cmvgcn16006l5y501irik14hk

Public deployment retained: Site version 7, Worker 0.1.3, source f71bc3d605b2e833cd442f4e664ad66ef552cac5. A2A reads the owner's portfolio; wallet execution remains explicitly user-approved.

This is a reviewable evidence packet, not certification of campaign eligibility. No campaign form was submitted in this audit. Final acceptance belongs to BNB Chain. Deadline: 5 November 2026 12:00 UTC / 19:00 Vietnam.
