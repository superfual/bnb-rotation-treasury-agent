# Public treasury invocation endpoint

Live URL: https://fual-treasury-agent.phamphuanloc.chatgpt.site

Public read-only Cloudflare Worker. GET /health, /.well-known/agent-card.json, /registration.json, /api/decision and /evidence. POST /a2a accepts stateless A2A 0.3.0 JSON-RPC message/send for status, decision, evidence. No streaming, task continuation, custody, signing, transaction submission or visitor-supplied wallet/RPC/targets.

Live decision checks the fixed chain-97 owner portfolio and pinned contracts. Results cache for at most 30 seconds; RPC failures return no decision, never fallback historical balances. Test pool reserve-ratio valuation is not a USD market price. Health checks service reachability only.

Run node tests/endpoint.test.mjs; add --live for a real read-only RPC check. Nine endpoint checks and live HOLD at 30.20% passed before deployment. Native deployment succeeded. Anonymous Chrome Incognito browser evidence on 15 October 2026 confirms the agent card and a real public POST /a2a message/send returned HTTP 200, matching request/reply IDs and fresh chain-97 data. This execution environment still receives HTTP 403 / 1010: arbitrary automated-client reachability remains unverified. The homepage includes a public A2A check button.

Registry reference: agent 370316 on chain 56. Mainnet ownerOf(370316) matched the campaign wallet. After the owner signed setAgentURI, a direct tokenURI read on 15 October 2026 returned https://fual-treasury-agent.phamphuanloc.chatgpt.site/registration.json. Original name, avatar, tags and TermiX metadata were preserved. Chain-97 activity attribution and campaign qualification remain unresolved. The signed transaction hash has not yet been retained; tokenURI state is independently verified. The private owner controller is separate.

Source deployment commit: 8ea13902280f621b8637834d4a6688fcde1a2c17. Official A2A reference: https://a2a-protocol.org/v0.3.0/specification/.
