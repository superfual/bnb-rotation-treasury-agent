# Set & Earn evidence and Build audit — 17 October 2026

Audit time: approximately 03:50 Vietnam / 16 October 20:50 UTC. Campaign wallet: `0xdcf64CdDC4a2b06F756f21a125ca393792DFA709`.

Official rules: https://www.bnbchain.org/en/hackathons/smart-money-era-set-and-earn . Deadline: 5 November 2026 12:00 UTC / 19:00 Vietnam. Organizer verification determines qualification and ranking. No prize or place is claimed here.

## Current conclusion

Three distinct buyer hires across Mandate and HelloFugu have retained payment evidence. A public-browser A2A invocation has passed with matching production semantic logs. Build remains incomplete: execution/category alignment, qualifying actions across three days, and independent qualifying customer usage remain unresolved. Campaign registration confirmation is not retained.

## Hire evidence

| Agent | Marketplace / chain | Purchase | Funding evidence | Result and limitation |
| --- | --- | --- | --- | --- |
| Yield-1 #344122 | Mandate / 56 | Job 57000, 0.01 U | [Successful funding](https://bscscan.com/tx/0x79fd0075074d2ad97ccfe80e68e88968da61313e7a3a639a88d12005d3b4d8b4) | Delivered read-only yield comparison. API SUBMITTED; no settlement tx. |
| Venus Rate Router #2556 | HelloFugu / 97 | Listing 25, subscription 24 | [Successful subscription](https://testnet.bscscan.com/tx/0xfae90f5a473e503006e788d165734c26246fb1f536f1b26d190ca07c4998d97e) | Provider release tx verified. A2A report call blocked by provider Cloudflare; support issue remains unresolved. |
| Guard-1 #344123 | Mandate / 56 | Job 57013, 0.01 U | [Successful funding](https://bscscan.com/tx/0x58ec0866d6c90c80d8b9590159caaa13c11511204658b93ac15b4320e91dee50) | Delivered no-Venus-position answer for campaign wallet. API SUBMITTED; no settlement tx. |

These are three different agents on two shortlisted marketplaces using the campaign wallet. No fourth purchase is proposed. An approval alone, unfunded Pokter jobs 1467/1468, quotes, and failed calls are excluded. The HelloFugu delivery limitation is retained honestly; final hire acceptance belongs to BNB Chain.

Mandate full API records, deliverables and successful funding/submission receipts: [2026-10-17-mandate-hires.json](2026-10-17-mandate-hires.json). HelloFugu subscription/release receipts: [2026-10-15-chain-audit.json](2026-10-15-chain-audit.json).

## Build — each official criterion

| Requirement | Verified evidence | Assessment |
| --- | --- | --- |
| ERC-8004 registration on 56/97, owned by campaign wallet, listed on shortlisted marketplace | Fresh mainnet ownerOf and tokenURI for #370316; TermiX listing cmv2uos8s0grdwx01t9j48xdi is PUBLISHED | Ownership and listing verified. Marketplace service currently says Market & Protocol Research. |
| Resolvable card describing function/category | Registered URI points to public registration.json; public card describes a read-only rebalancing prototype; external collectors received HTTP 200 | Discovery observed. Actual marketplace offer and prototype have different scopes that must be reconciled truthfully. |
| Responds when invoked | Public browser message/send succeeded 17 October 03:37:09 Vietnam; matching response IDs, fresh chain-97 data, HOLD 30.2%, semantic production log rpcSuccess true | External-browser invocation passed. Some automated callers, including this checker, remain Cloudflare-1010 blocked. Random organizer probes are not guaranteed. |
| Three completed hires from distinct wallets not owned/funded by builder | Three TermiX research orders SETTLED; settlement receipts successful; three distinct buyer addresses, none equal owner | Completed commerce verified. Independence of funding and qualification of research work for this rebalancing prototype remain unconfirmed. Do not call this criterion complete. |
| At least five own-agent onchain actions on at least three separate days | Three successful swaps, all 13 October; one manual and two owner-approved controller swaps | Insufficient action/day coverage even if all three were accepted. Agent attribution of owner-signed cross-chain actions remains unconfirmed. |
| Actions match declared category; repository public | Public repo; private owner controller prepares bounded treasury adjustments; public endpoint is read-only | No unattended signer or production execution session. Report delivery, escrow settlement, approval, buyer hire and A2A reads are not counted as rebalancing. |

Identity: [2026-10-17-identity.json](2026-10-17-identity.json). Actions: [2026-10-17-action-inventory.json](2026-10-17-action-inventory.json). Provider orders: [2026-10-17-provider-orders.json](2026-10-17-provider-orders.json). Public A2A: [2026-10-17-a2a-production-success.json](2026-10-17-a2a-production-success.json) and [invocation audit notes](2026-10-17-external-invocation-notes.md).

## Customer orders: current verified state

| Order | Buyer wallet | Status | Onchain settlement |
| --- | --- | --- | --- |
| cmv567tc5t71qzw01aoaapovm | 0xf0a15d3d9a5350108015733ab665255bfeb1653c | SETTLED | [12 October](https://bscscan.com/tx/0x6cccbb66f9768d852dd829dc07fb460bf178db921a0177a88e804561e3affe69) |
| cmv5ch14ltwauzw01qbwi7t90 | 0xab1c3c80e756f407588408a86743c730bf057208 | SETTLED | [12 October](https://bscscan.com/tx/0x631626719d493c85a9a88cc4b145797e9c975d1d52a99af603d1ea327562f7ac) |
| cmvaluzar08qlw701y5nhx3gh | 0xe4833de51a818b68f5a074b68bcdac82e7349adc | SETTLED | [16 October](https://bscscan.com/tx/0x59aab4601eb2147bf5cbb440db7a37086b01e83e9aa3b750a9d7e6822308eb55) |

Each receipt transfers 1.96 USDC (18 decimals) to campaign wallet and 0.04 USDC to the protocol destination. Total receipts to wallet are 5.88 USDC, before the owner's gas/other expenses, not net profit. BlueToken's published review is 5/5. Backend fields disagree on nominal providerPayout (2) versus protocolFee (0.04); actual ERC-20 receipt transfers govern the 1.96 figure. Raw private report links and buyer messages are excluded from public evidence.

## Remaining work in dependency order

Implementation update, 17 October 04:02 Vietnam: the owner-private controller now verifies registry owner/URI before preparing and signing, binds reviewed plans to the identity observation and fixed policy, and records/export decisions and receipt proofs. The new flow has passed unit/fake-wallet and real-RPC module checks and is deployed. See [controller identity journal](2026-10-17-controller-identity-journal.md). This is a controller provenance improvement, not onchain agent attestation; prior trades are not retroactively reclassified and no extra action/day is counted.

1. Implement a coherent rebalancing service under the existing agent identity, with bounded execution, explicit user authority, durable decision/action records and clear listing terms. Preserve the research service's actual historical scope; do not relabel completed reports as automatic trades or register a cosmetic clone.
2. Tie controller execution to identity #370316 on chain 56 with reviewable evidence. The execution chain is 97. Confirm this attribution with organizer requirements before counting historical swaps.
3. Accumulate genuine category-consistent actions on the required separate dates when the strategy warrants them. Current fresh result is HOLD at 30.2%; it does not justify extra trades. No artificial drift, circular flows or counter-filling trades.
4. Establish independent customer usage of the qualifying function and document funding independence. Do not fund customers, self-hire or manufacture jobs.
5. Retain campaign registration confirmation and ensure public GitHub exposes the identity ID/chain and evidence index. Keep automated-client Cloudflare access as an explicit residual limitation.

No transaction, token approval, customer message, marketplace service change or customer-wallet funding was performed in this audit. Existing draft PR stays draft; no merge is authorized or performed.
