# Public invocation audit — 17 October 2026 (Vietnam)

## Final result: external browser A2A success confirmed

At 17 October 03:37:09 Vietnam, the user's desktop browser called the public production /a2a endpoint. Screenshot libfile_b7e14d5dda8c81918289a879b3600992 shows A2A success, HTTP 200, matching request/reply ID 05c6d1ad-39ad-45d4-861e-fa6f01057374, chain 97, observedAt 2026-10-16T20:37:09Z, block 0x82d5e98, HOLD and WBNB 30.2%.

Independent production audit event confirms rpcSuccess true, readOnly true, chainId 97, same observation time/block and HOLD, version 0.1.2. Worker request ID 881614427b8ad0a55e06c397287d4b30; ray a4b9dc1e4be584bd; audit probe ID ac36e434-95fb-4ce5-b718-ad0a09e0c905. The associated POST /a2a has HTTP 200/outcome ok. Sanitized proof: 2026-10-17-a2a-production-success.json.

The external browser invocation check is now passed. This does not establish unrestricted access for all automated callers: the execution environment's Cloudflare 1010 remains. No transaction was sent and campaign Build qualification as a whole remains unconfirmed.

The historical 'pending' statements below describe the earlier audit stages and are superseded by this final result.

Site: https://fual-treasury-agent.phamphuanloc.chatgpt.site

Sites confirmed the existing publication is active, public, version 4. No access settings or source code were changed.

An anonymous HTTP client in this execution environment requested GET /.well-known/agent-card.json, GET /health, and POST /a2a with a read-only JSON-RPC message/send status request. All three were rejected with HTTP 403, Cloudflare error 1010. This is an edge rejection, not an application JSON-RPC error. No alternate client identity, bypass token, proxy, or repeated workaround was used.

Production logs independently show outside clients retrieving /registration.json and /.well-known/agent-card.json with HTTP 200. A client identifying itself as agent-collector/0.1 sent POST /a2a at 2026-10-16T19:39:35.257Z (17 October 02:39:35 Vietnam); Worker outcome ok, HTTP 200, wall time 205 ms, request ID fcb9493f49d5c74f16136f8e70691a75, ray a4b987c7f9375704. User-Agent is self-declared, not verified organizational identity.

This establishes external discovery and an external POST receiving an application response. Logs do not include its request or response body: JSON-RPC success, a fresh portfolio decision, and complete message/send delivery are NOT proven by HTTP 200. A JSON-RPC error can also use HTTP 200. General automated-client access remains limited by Cloudflare 1010 for this checker.

Probe responses and request payload: 2026-10-17-external-invocation.json. Selected sanitized event metadata: 2026-10-17-external-worker-events.json. No wallet transaction or signing occurred.

## Follow-up implementation

Published Site version 5 / Worker card version 0.1.2, source 78a2bb8df8d335ee0b095b13f4d4c8643c2ea410, deployment appgdep_6ad28a7d1cd88191bac48c73faa545e3 succeeded at 2026-10-16T20:35:29Z. Audience remains public.

Every A2A response now emits a bounded semantic audit event: HTTP status, JSON-RPC success or error code, generated probe ID, and (for fresh status replies) chain, block, decision and observation time. Caller request text/IDs and headers are not logged. A regression check confirms HTTP-200 JSON-RPC errors are distinguished from successful agent replies and request input is omitted. Existing endpoint/discovery checks, a fresh Testnet read, artifact validation, and the audit check passed.

A direct invocation of the local Worker module using actual BSC Testnet RPC completed message/send status with matching reply ID and role agent; observedAt 2026-10-16T20:35:39Z, block 0x82d5dce, HOLD, WBNB 30.2%. This is real-chain functional verification, not an external HTTP probe.

The existing public page button 'Kiểm tra A2A công khai' sends the canonical message/send status request and validates its JSON-RPC ID, agent reply and chain-97 data. The remaining user-browser probe can establish semantic production success without a wallet connection, access bypass or payment. Do not mark that final public-browser probe passed until its response or production audit event is observed.
