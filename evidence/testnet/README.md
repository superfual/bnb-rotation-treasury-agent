# BSC testnet owner execution evidence

On 13 October 2026 at 08:39:46 UTC (15:39:46 Vietnam), the owner signed a
PancakeSwap V2 swap through BscScan inside Binance Wallet. This is a manual
owner-reviewed testnet execution, not unattended agent execution or a proof
of campaign qualification.

- Chain: 97; owner: `0xdcf64CdDC4a2b06F756f21a125ca393792DFA709`.
- Transaction: [BscScan receipt](https://testnet.bscscan.com/tx/0xf4c9421b4b9c99bd0448505a2d7a187119db65ffc422ec51bcb646f876d9e3c4).
- Input: exactly 1 test U; output: 0.005040429466318224 test WBNB.
- Minimum output reviewed: 0.005015227318986632 test WBNB.
- Native value: zero. Actual gas fee: 0.000017816964 tBNB.
- Post-swap balances: 9 test U and 0.005040429466318224 test WBNB.
- Exact U allowance to the router is now zero.

The receipt status, sender, router, complete calldata, zero native value,
gas cap, both token Transfer logs, output floor, balances and canonical block
hash were checked by public RPC. The canonical block was rechecked after
549 confirmations. See the JSON record for exact raw amounts. This is a
snapshot, not a permanent guarantee of finality or a general automated
reconciliation implementation.

## Manual review boundary

The mobile manual flow used a one-hour transaction deadline after shorter
windows proved impractical. Exact input, output floor and gas cap remained
bounded. This extended manual deadline is separate from the adapter policy,
which still caps generated plans at 300 seconds. The manually reviewed call
was independently simulated, matched to the receipt and reconciled. Do not
claim that the 180-second planner or the undeployed HTML signing page executed
this transaction.

## Next observed decision

Reserve-ratio valuation put WBNB at 10.04% of the two-token test treasury,
below the configured 30% target and outside the five-percentage-point drift
band. A further buy is a candidate, not an executed instruction: it requires
fresh reads, simulation and a new exact allowance approved by the owner.
Native tBNB is reserved for gas and excluded from the two-token allocation.
No new transaction was sent and no private key/session was granted.

Existing agent identity 370316 remains on chain 56. Attribution of this
owner-wallet chain-97 swap to that identity, a public live agent endpoint,
independent marketplace hires and campaign eligibility remain unresolved.
