# Public treasury invocation endpoint

Live URL: https://fual-treasury-agent.phamphuanloc.chatgpt.site

Public read-only Cloudflare Worker. GET /health, /.well-known/agent-card.json, /registration.json, /api/decision and /evidence. POST /a2a accepts stateless A2A 0.3.0 JSON-RPC message/send for status, decision, evidence. No streaming, task continuation, custody, signing, transaction submission or visitor-supplied wallet/RPC/targets.

Live decision checks the fixed chain-97 owner portfolio and pinned contracts. Results cache for at most 30 seconds; RPC failures return no decision, never fallback historical balances. Test pool reserve-ratio valuation is not a USD market price. Health checks service reachability only.

Run node tests/endpoint.test.mjs; add --live for a real read-only RPC check. Nine endpoint checks and live HOLD at 30.20% passed before deployment. Native deployment succeeded. External anonymous HTTP reachability is NOT verified: this execution environment received a timeout and HTTP 403. Native access policy reports public; do not treat this as proof of external bot reachability until independently probed.

Registry reference: agent 370316 on chain 56. The registry URI/domain has NOT been updated or verified to point here; chain-97 activity attribution and campaign qualification remain unresolved. /registration.json is a proposed registration document, not a transaction. The private owner controller is separate.

Source deployment commit: 2ba31ec8130ac0b4f5bf53e2c51dc45853ec0218. Official A2A reference: https://a2a-protocol.org/v0.3.0/specification/.
