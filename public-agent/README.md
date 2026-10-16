# Public treasury invocation endpoint

Customer-wallet Testnet beta: https://fual-treasury-agent.phamphuanloc.chatgpt.site/rebalance/ . Free, explicit customer approval, no marketplace order or autonomous server signing. See ../docs/CLIENT_TESTNET_BETA.md. Worker 0.1.3 / Site version 6 deployment source b4d0b48fadc1104ba7c1501de6f0f6ce30181043. Original owner A2A invocation remains read-only.

`client-ui/` contains the five served beta assets; `scripts/build-client-assets.mjs` deterministically embeds them in the Worker. Re-run it before route tests/deployment when those assets change. Client engine/UI, route and receipt reconciliation tests live in `tests/client-*`. From this directory, `node scripts/verify-client-journal.cjs <exports...>` checks chain-97 receipts and candidate date counts without signing. Publication and HOLD do not add paid hires or execution days.

Live URL: https://fual-treasury-agent.phamphuanloc.chatgpt.site

Public read-only Cloudflare Worker. GET /health, /.well-known/agent-card.json, /registration.json, /api/decision and /evidence. POST /a2a accepts stateless A2A 0.3.0 JSON-RPC message/send for status, decision, evidence. No streaming, task continuation, custody, signing, transaction submission or visitor-supplied wallet/RPC/targets.

Live decision checks the fixed chain-97 owner portfolio and pinned contracts. Results cache for at most 30 seconds; RPC failures return no decision, never fallback historical balances. Test pool reserve-ratio valuation is not a USD market price. Health checks service reachability only.

Run node tests/endpoint.test.mjs; add --live for a real read-only RPC check. Nine endpoint checks and live HOLD at 30.20% passed before deployment. Native deployment succeeded. Anonymous Chrome Incognito browser evidence on 15 October 2026 confirms the agent card and a real public POST /a2a message/send returned HTTP 200, matching request/reply IDs and fresh chain-97 data. This execution environment still receives HTTP 403 / 1010: arbitrary automated-client reachability remains unverified. The homepage includes a public A2A check button.

Registry reference: agent 370316 on chain 56. Mainnet ownerOf(370316) matched the campaign wallet. After the owner signed setAgentURI, a direct tokenURI read on 15 October 2026 returned https://fual-treasury-agent.phamphuanloc.chatgpt.site/registration.json. Original name, avatar, tags and TermiX metadata were preserved. Chain-97 activity attribution and campaign qualification remain unresolved. The signed transaction hash has not yet been retained; tokenURI state is independently verified. The private owner controller is separate.

Source deployment commit: 8ea13902280f621b8637834d4a6688fcde1a2c17. Official A2A reference: https://a2a-protocol.org/v0.3.0/specification/.

## 15 October discovery compatibility correction

Production request logs showed external probes reaching the worker but using
`POST /.well-known/agent-card.json` and `POST /a2a/a2a`; both previously returned
405. The card now explicitly advertises `supportedInterfaces` for `/a2a`.
Those observed POST aliases and a trailing-slash `/a2a/` route run the same
JSON-RPC validator as `/a2a`. They expose no additional command or signing
capability. HEAD and an allow-all robots.txt are supported for discovery.
`node tests/discovery.test.mjs` covers these observed paths and confirms that
trade methods and invalid message roles remain rejected on every alias.

Publication succeeded from source commit
`1b175f32ab433689a18f5888980def4d803b0bed`. The correction is not proof that
all external probes pass: a new successful production invocation is still
needed. Platform Cloudflare 1010 restrictions cannot be removed in worker
application code. Do not spoof clients or retry a non-retryable block.

## 17 October verified public-browser invocation

Worker 0.1.2 / Site version 5 adds bounded semantic A2A response logs, excluding caller text, request IDs and headers. The audit regression check distinguishes HTTP-200 JSON-RPC errors from successful agent messages. Run `node tests/a2a-audit.test.mjs`.

The external user-browser probe at 2026-10-16T20:37:09Z passed: status message/send returned fresh chain-97 data, HOLD and WBNB 30.2%, with matching request/reply IDs. Production audit logged rpcSuccess true and the same block/time. Evidence: `../evidence/testnet/2026-10-17-a2a-production-success.json`. This supersedes the earlier pending-probe wording. The checker's Cloudflare 1010 persists; general automated-client reachability is still limited.

Current deployment source: `78a2bb8df8d335ee0b095b13f4d4c8643c2ea410`.
