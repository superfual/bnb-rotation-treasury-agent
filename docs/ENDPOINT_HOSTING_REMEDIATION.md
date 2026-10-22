# Public A2A hosting remediation — 22 October 2026

Status: **OPEN**. Source compatibility fixes are deployed in Site version 8; normal Python public access still returns HTTP 403 / Cloudflare 1010. Do not claim the endpoint is universally inaccessible: production logs also contain successful discovery requests from other clients.

## Ready-to-send hosting support request

Subject: Public Sites A2A endpoint blocked with Cloudflare 1010 for normal machine clients

Please investigate the Cloudflare security event for this public Site:

- Host: `fual-treasury-agent.phamphuanloc.chatgpt.site`
- Sites project: `appgprj_6ace389509e08191b0e4caee309ce76f`
- Production version: 8; source `05c44c657a1de4b2ae33ef58eb162c23adaa0ea5`
- Request: `GET /a2a`, Python standard-library urllib, no authentication or cookies
- Observed: **2026-10-22 16:54:15 UTC**
- Response: HTTP 403, body `error code: 1010`
- CF-Ray: **a4ea05d81adb6c04-DFW**

The API is intentionally public and read-only. Its discovery and JSON-RPC callers cannot solve browser challenges. Please identify the actual matched security rule using the Ray ID; confirm whether Browser Integrity Check is responsible. If confirmed, configure a narrowly scoped exception for this hostname's API/discovery paths. Keep other protections and application limits enabled. Do not require a private access token for public agent discovery.

Candidate configuration rule, to be reviewed and applied by the zone administrator only:

```text
(http.host eq "fual-treasury-agent.phamphuanloc.chatgpt.site" and
 http.request.uri.path in {"/a2a" "/registration.json" "/.well-known/agent-card.json" "/.well-known/agent-registration.json"} and
 http.request.method in {"GET" "HEAD" "POST" "OPTIONS"})
```

Action: `set_config`; action parameters: `{ "bic": false }`.

This is a proposed rule, not an applied change or proof of the matched rule. If another security product causes the block, investigate that event rather than disabling unrelated protections.

## Acceptance criteria

Run `python3 public-agent/scripts/check-public-access.py` from at least two independent normal machine-client environments. It must exit 0: card/registration/discovery return JSON, and `POST /a2a` with `message/send` and `evidence` returns a valid agent result. No browser session, authentication cookie or spoofed browser identity should be needed. Verify a live `status`/`decision` separately, including fresh chain data and fail-closed RPC behavior; a static evidence reply does not prove live RPC access. Preserve a timestamped result after the host fix. Do not send transactions as an access test.

## Ownership and fallback

The available Sites management interface does not expose Cloudflare zone security settings. The Site author cannot apply this proposed edge rule through those tools. Application JavaScript cannot repair a rejection that occurs before it runs.

If the platform cannot support ordinary public API clients, deploy the existing Worker as an actual origin on hosting controlled by the owner, with an API-compatible security policy. This requires an authorized hosting account and deployment access. It is not a forwarding proxy around the current block. Keep the old endpoint until the new origin passes acceptance, then update the ERC-8004 registration URI and discovery URLs through an owner-approved transaction. Do not claim migration or change on-chain identity before those actions occur.

Sources:
- https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-1xxx-errors/error-1010/
- https://developers.cloudflare.com/waf/tools/browser-integrity-check/
- https://developers.cloudflare.com/rules/configuration-rules/settings/

This document contains no session cookies, credentials, customer reports or private headers. The support request is prepared, not sent.
