# Set & Earn evidence and Build audit — 22 October 2026

This is the current evidence index. It replaces outdated live-status statements in earlier revisions; dated JSON evidence retains its original observation time. Organizer qualification is not claimed.

Campaign wallet: `0xdcf64cddc4a2b06f756f21a125ca393792dfa709`. Identity: **ERC-8004 #370316, chain 56**. Execution chain: **97**.

Official rules: https://www.bnbchain.org/en/hackathons/smart-money-era-set-and-earn . Deadline: **5 November 2026, 12:00 UTC / 19:00 Vietnam**. Registration must precede qualifying tasks. The final qualifying onchain timestamp determines provisional position; organizer verification determines acceptance.

## Latest update — 22 October 2026

- **MGent order cmvibjeiz2lce0z0168hnf5dv is SETTLED.** Fresh chain-56 receipt status is 1, with 1.96 USDC to the campaign wallet and 0.04 USDC protocol fee. [Settlement audit](2026-10-22-mgent-settlement.json). The delivered report confirms a within-band final portfolio observation and discloses missing individual swap hashes/original browser journal. This is a completed paid engagement; its settlement is not counted as a rebalance swap. No further customer proof requests are required.
- Completed commerce is now **six orders from six distinct buyer addresses**, totaling **11.76 USDC received before expenses**. Independent control/funding is still not certified.
- **Five historical candidate swaps on three dates were re-read against canonical transactions, receipts and blocks.** [Fresh execution recheck](2026-10-22-execution-recheck.json). No action/day was added. This strengthens receipt evidence, not original signing provenance.
- **Public Site version 8 deployed**, source `05c44c657a1de4b2ae33ef58eb162c23adaa0ea5`. GET /a2a now returns discovery data and POST message/send instructions; it does not return a synthetic live decision. The conventional /.well-known/agent-registration.json redirects to /registration.json. POST semantics remain fail-closed.
- Production logs show repeated successful card/registration GETs from external clients; some probes used GET /a2a and previously received 405. The route compatibility fix is deployed and four test files passed. **Normal Python requests after deployment still receive 403.** General automated-caller access remains unresolved; no platform firewall modification or bypass is claimed. [Sanitized production observations and deployment](2026-10-22-endpoint-audit.json).

## Current requirement matrix

| Requirement | Evidence and result | Remaining limitation |
| --- | --- | --- |
| Three different buyer hires across two shortlisted marketplaces | Mandate Yield-1 #344122/job57000; Mandate Guard-1 #344123/job57013; HelloFugu Venus Rate Router #2556/sub24. Additional Pokter Nagi #2623/job1564 funded and public UI settled | HelloFugu provider A2A report call failed; retained honestly. These are hire-event/payment records, not rebalance actions |
| Registered, owned and listed | Fresh owner/registered URI check for #370316; published TermiX research and owner-approved Testnet support listings | Registry identity is on 56, execution on 97; marketplace provider metadata has stale URI/A2A fields |
| Discoverable card and declared category | Registered URI and historical reachable card declare rebalancing with explicit owner approval | Fresh automated HTTP checks are blocked, so current general reachability is not established |
| Live invocation | Historical browser A2A success and matching semantic production logs on 17 October | 21 October external requests received Cloudflare 403/1010; unresolved |
| Three completed hires from distinct independent wallets | Six retained SETTLED orders from six different buyer wallets: three research orders plus three portfolio/rebalancing-support orders | Different addresses alone do not prove independent control/funding; independence is not certified |
| At least five actions across three days | **Five canonical successful candidate swaps on 13, 20 and 21 October** | Agent attribution is not certified; original recent signing journals missing; one historical swap manual |
| Category-consistent execution / public source | WBNB/U adjustments, bounded 30/70 policy, public repository and explicit assisted-execution terms | No autonomous signer is claimed. Capital-addition test context disclosed |
| Campaign registration | Owner screenshot confirms official form already responded, with BNB Chain thank-you message | Submitted wallet/agent fields and original timestamp are not visible |

The official completed-hire clause does not explicitly require every hire to execute a swap. Research, partial-support and HOLD jobs retain their true delivered scope; they are not rewritten as completed automated rebalances. Onchain execution/category evidence is presented separately. Final applicability is for the organizer to decide.

## Execution inventory

[Five-action inventory](2026-10-21-action-inventory.json), [21 October receipt reconciliation](2026-10-21-owner-rebalance.json), [raw canonical receipt](2026-10-21-owner-rebalance-receipt.json), [attribution review](2026-10-21-attribution-audit.md).

| Date, Vietnam | Successful swaps | Context |
| --- | --- | --- |
| 13 October | 3 | One manual, two controller-approved historical swaps |
| 20 October | 1 | Explicit 0.005 tBNB capital-addition Testnet scenario; WBNB reduced to 29.77%, HOLD |
| 21 October | 1 | Explicit 0.005 tBNB capital-addition Testnet scenario; WBNB reduced to 29.80%, HOLD |

Latest swap: [0x382f9c…92951](https://testnet.bscscan.com/tx/0x382f9caabbcbe3f1d33334d71d31661f8d420c1589ca12f073e14e2414392951), **21 October 14:00:06 Vietnam**, **0.003649802933723126 WBNB → 0.799078319423714694 U**, fee **0.000014955864 tBNB**. Original pre-sign browser journal is not supplied. The recent exported JSON is stale, containing only historical HOLD; no retrospective signing proof was invented.

Wraps, approvals, hire payments, deliveries, settlements, HOLD/read-only calls and duplicate hashes are excluded from swap/action counts. No further trade is warranted merely to increase these counters.

## Completed customer commerce

[Three historical research orders](2026-10-17-provider-orders.json); [two additional settled support orders and fresh settlement receipts](2026-10-21-settled-orders.json).

| Order | Original scope | Current retained state |
| --- | --- | --- |
| cmv567tc5t71qzw01aoaapovm | Research | SETTLED, 12 October |
| cmv5ch14ltwauzw01qbwi7t90 | Research | SETTLED, 12 October |
| cmvaluzar08qlw701y5nhx3gh | Research | SETTLED, 16 October |
| cmvgptyf39r1iro0148jqq29w | Owner-approved Testnet support; partial report with final target unverified | SETTLED, 21 October; buyer accepted the disclosed report |
| cmvhpqp9o0bxgue01b58keqcn | Paid portfolio review; HOLD/no swap warranted | SETTLED, 21 October |
| cmvibjeiz2lce0z0168hnf5dv | Portfolio/rebalancing support; final state verified, per-swap proofs missing and disclosed | SETTLED, 22 October |

Each retained settlement paid **1.96 USDC** to the campaign wallet and **0.04 USDC** protocol fee; six orders total **11.76 USDC received before expenses**, not net profit. Private reports, messages and customer portfolio balances are excluded. Customer approval-only transactions are not described as completed swaps.

## Buyer-hire evidence

| Agent / marketplace | Onchain evidence | Retained result |
| --- | --- | --- |
| Yield-1 #344122 / Mandate, 56 | [Fund job57000](https://bscscan.com/tx/0x79fd0075074d2ad97ccfe80e68e88968da61313e7a3a639a88d12005d3b4d8b4) | Read-only report submitted; settlement not retained |
| Guard-1 #344123 / Mandate, 56 | [Fund job57013](https://bscscan.com/tx/0x58ec0866d6c90c80d8b9590159caaa13c11511204658b93ac15b4320e91dee50) | Answer submitted; settlement not retained |
| Venus Rate Router #2556 / HelloFugu, 97 | [Subscription24](https://testnet.bscscan.com/tx/0xfae90f5a473e503006e788d165734c26246fb1f536f1b26d190ca07c4998d97e) | Provider payment release verified; A2A report call unresolved |
| Nagi #2623 / Pokter, 97 | [Fund job1564](https://testnet.bscscan.com/tx/0x08b6dd8b9609f0c3e848364a2e704ed6ea98776e373c1f30ddf976e47a8acc15) | Public UI settled 20 October; buyer reported report/review completed |

[Mandate records](2026-10-17-mandate-hires.json), [HelloFugu audit](2026-10-15-chain-audit.json), [Pokter audit](2026-10-20-pokter-nagi-hire.json). Unfunded old Pokter jobs, quotes and approvals are not hires.

## Identity, service and external access

[Fresh identity](2026-10-21-identity.json). [Published assisted service](2026-10-20-rebalancing-service.json): https://www.agent.family/listing?id=cmvgcn16006l5y501irik14hk . Same agent identity, 2 USDC / one day, custom agreed scope, each wallet transaction requires user approval. The research service remains research. A free beta visit is not a paid hire.

Public Site version 8, source `05c44c657a1de4b2ae33ef58eb162c23adaa0ea5`; Worker protocol metadata remains 0.1.3. GET discovery compatibility is documented in the latest update. [17 October browser A2A success](2026-10-17-a2a-production-success.json); [21 October external checks](2026-10-21-external-check.json). The public read-only endpoint and customer-wallet execution are separate. No current blanket availability guarantee is made.

## Remaining evidence gaps

1. **Original signing provenance / attribution:** preserve the real browser journals if recoverable; canonical receipts and reconstructed plans do not replace them. Review chain-56 identity / chain-97 owner-approved execution attribution.
2. **Public endpoint access:** Cloudflare 403/1010 blocks today's normal automated probe. Hosting-level access remains unresolved; no bypass was attempted.
3. **Registration field check:** [official-form screenshot review](2026-10-21-registration-review.md) confirms an existing response. Submitted wallet/agent fields and original timestamp remain unseen. Compare them in the existing edit-response page; keep its URL private. No duplicate form was submitted.
4. **Customer independence:** six completed orders are documented, but independent ownership/funding has not been certified. Do not fund customers or create substitute self-hires.

This audit signed no transaction, sent no customer message and made no new hire or campaign submission. The existing draft PR remains unmerged. The five-swap/three-day numerical record is supported; automatic qualification or a prize is not asserted.
