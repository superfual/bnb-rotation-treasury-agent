# Identity-linked owner-approved controller — 17 October 2026

Private owner controller: https://fual-treasury-control.phamphuanloc.chatgpt.site

Source 6be279fe4544b86e88e8945001eae7b267906414 deployed successfully at 2026-10-16T21:01:59Z (17 October 04:01:59 Vietnam), Site version 3. Deployment appgdep_6ad290b1d59881918cd08885fae18e3f. Audience remains owner-private.

## Implemented

- Read chain-56 ERC-8004 ownerOf(370316), tokenURI and canonical block at preparation and again before the wallet transaction request. Require fixed owner and registered public URI, correct identity chain and fresh head; unavailable or changed identity prevents signing.
- Bind a SHA-256 plan digest to the observed identity, original fixed execution policy and actual pre-sign transaction. Transactions remain chain 97, one exact owner approval at a time. Mainnet calls only read identity.
- Persist decisions, sign requests, broadcast hashes and independently verified confirmations in the browser. The journal links hashes to detect accidental edits and exports JSON. Input/output/fee/receipt data remains linked to its retained reviewed plan.
- Preserve pending state on ambiguous wallet results and on a confirmed-receipt journal save failure. A legacy pending request can be reconciled but remains explicitly unbound. Original limits and exact approvals remain unchanged.

## Validation

Sixteen engine checks and twelve fake-wallet UI checks pass. New evidence checks cover wrong chain/owner/URI, stale identity data, tampered plans/journals, duplicate receipt IDs and storage failure. Static JavaScript parses successfully. Direct module smoke check against real chain 56 and 97 returned identity #370316 verified and HOLD at WBNB 30.2%, without broadcasting: 2026-10-17-controller-binding-smoke.json. Browser visual QA was unavailable because control-browser is not installed; the new journal/identity flow has not yet been tested in the owner's actual mobile wallet.

## Limits and qualification

User-browser follow-up passed at 17 October 04:04:49 Vietnam: exported journal has one DECISION entry, identity #370316 on chain 56 / execution chain 97, HOLD at 30.2%. The verifier accepted the journal hash chain and re-derived the plan digest after decoding exact integer values. See 2026-10-17-controller-browser-journal-check.json for the source file SHA-256 and checked metadata. This verifies the new preparation/export path in the user's browser, not an actual new wallet transaction or post-trade journal. No action/day is added.

This is local controller provenance, not a signature or attestation from the ERC-8004 registry and not a smart-contract-enforced attribution. A determined local editor can recompute hashes. Browser storage can be deleted and is not remote durable storage; export before clearing or switching devices. No unattended signer, session grant or aggregate daily budget enforcement was added. Previous swaps are not retroactively attributed.

No action is needed while allocation remains inside the drift band. This deployment adds no swap day, customer engagement, or qualifying execution. Category alignment, genuine independent customer usage, action/day coverage and organizer acceptance remain unresolved.
