# Mobile evidence export fix — 17 October 2026

Customer reported that the Binance Wallet browser did not download the journal. The prior handler attempted a Blob download and immediately claimed success without knowing whether the browser saved it.

The public beta now displays the complete validated journal in a selectable read-only text area first. Clipboard copying is explicit and falls back to manual selection. File download is optional and described as a request, not confirmed completion. Valid transaction hashes in the journal are deduplicated and exposed as BscScan links; invalid link inputs are omitted. The export performs no signing, RPC request, remote upload, storage mutation or journal deletion. Existing storage keys remain unchanged.

Published Site version 7, deployment appgdep_6ad3583698e081918d0c5309a1cfe895, source f71bc3d605b2e833cd442f4e664ad66ef552cac5, succeeded 2026-10-17T11:13:06.177544Z. Public URL: https://fual-treasury-agent.phamphuanloc.chatgpt.site/rebalance/ .

Validation passed: mobile export regression with unavailable clipboard/blocked Blob download, exact selectable JSON retention, safe transaction links and no false completion message; existing client engine, UI, route, A2A/discovery and endpoint checks. Native publication succeeded. Real Binance Wallet post-fix export remains awaiting customer confirmation; managed visual QA was unavailable. No execution/day/hire count is added by this fix. Customer messages and attachments are not included in this public evidence.
