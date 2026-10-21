# Execution attribution review — 21 October 2026

Identity: ERC-8004 #370316 on chain 56. Owner/controller wallet: `0xdcf64cddc4a2b06f756f21a125ca393792dfa709`. Execution: chain 97. [Fresh registry check](2026-10-21-identity.json).

## What is supported

- The controller and public client engine use the same 30% WBNB / 70% U policy, 5pp drift band, maximum 1 U notional per trade, 0.5% slippage and 0.0001 tBNB gas ceiling.
- `public-agent/client-ui/evidence.js` binds plan digests to the identity, owner and registered URI. The deployed private controller source checks identity before preparation/signing, writes SIGN_REQUESTED before requesting the wallet, then BROADCAST and CONFIRMED after reconciliation. These are implementation observations, not proof that a specific historical browser ran that exact flow.
- The 21 October [canonical receipt](2026-10-21-owner-rebalance-receipt.json) proves a successful owner-to-router WBNB/U swap. [Reconciliation](2026-10-21-owner-rebalance.json) checks actual transfers, minimum output, canonical block, deadline, gas and confirmations. The plan used for this reconciliation was reconstructed from actual calldata; it is not represented as the original pre-sign plan.
- Retained pre-sign preparation observed a 0.003649802933723126 WBNB amount, matching the actual swap input. The subsequent retained portfolio observation was 29.80% WBNB, HOLD. That preparatory observation alone is not a signed controller journal.
- Both 20 and 21 October scenarios were explicitly disclosed owner capital-addition Testnet tests. Neither is represented as organic market drift. Wraps/approvals are excluded.

## What is still missing

The supplied file named `fual-agent-370316-evidence-2026-10-21T07-01-07-070Z.json` has SHA-256 `1f7477286706d34adb733d2e51bc71f5abb3ff9f1e803d7ff7e14f7b09bbae78`, identical to the prior stale export. It contains one historical HOLD and zero verified receipts. It does not attest to the 20/21 October signing flow. No retrospective journal was generated or substituted.

The inventory contains five successful candidate swaps on three dates. One 13 October trade was manually signed; the others are described as owner-approved controller activity. There is no unattended agent signer or onchain identity attestation. Acceptance of these owner-signed chain-97 actions for the chain-56 identity remains for organizer review. Receipt success alone does not certify agent attribution.

## Reachability

[Normal external HTTP checks](2026-10-21-external-check.json) returned Cloudflare HTTP 403 / code 1010 for the card, registration URI and POST /a2a. A separate web reader also could not access the card/registration URI. No bypass was attempted and no platform-level firewall settings were changed. [17 October browser invocation](2026-10-17-a2a-production-success.json) remains a valid historical success, not proof of general availability today.

Public-client availability is an open deployment-hosting issue; this audit does not claim it was fixed. The read-only A2A endpoint and owner-approved wallet execution are separate interfaces.
