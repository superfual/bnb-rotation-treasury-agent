# Guarded Binance Spot Execution Roadmap

V1 is paper-only. A future deployment can route qualified portfolio decisions to a dedicated, manually funded Binance Agentic sub-account while preserving a human authorization boundary.

## Proposed flow

```text
Validated closed-candle snapshot
→ BNB regime and candidate gates
→ Paper target portfolio
→ Spot execution preflight
→ Immutable order proposal
→ Human confirmation
→ Spot-only order adapter
→ Order-status reconciliation
→ Balance and exposure verification
→ Audit evidence
```

## Required controls

1. **Isolated capital** — use only a dedicated Agentic sub-account funded manually with an explicit loss budget.
2. **Tool allowlist** — permit Spot market data, account reads, exchange rules, Spot order placement, and Spot order queries only.
3. **Tool denylist** — reject Margin, Futures, Convert, withdrawal, and cross-wallet transfer calls regardless of upstream permissions.
4. **Fresh preflight** — re-check symbol status, `LOT_SIZE`, `PRICE_FILTER`, `NOTIONAL`, balance, fees, exposure, and decision age immediately before proposing an order.
5. **Immutable proposal** — bind symbol, side, type, amount, maximum slippage, decision time, snapshot hash, and expiry into the confirmation request.
6. **Human confirmation** — no write call until the user approves the exact current proposal. A changed or expired proposal requires a new confirmation.
7. **Idempotency** — use a deterministic client order ID and query before retrying after an uncertain response.
8. **Reconciliation** — verify fills, commissions, residual balances, open orders, and resulting portfolio weights.
9. **Circuit breakers** — cap order value, daily turnover, concurrent positions, portfolio drawdown, and data age.
10. **Emergency stop** — block new proposals, cancel eligible open Spot orders, disconnect the agent, and preserve evidence.

## Separation of responsibilities

The analytical engine may produce `ROTATION_READY` or `ROTATE_OUT`; it cannot call an exchange. The execution adapter may translate an approved target into a valid Spot order; it cannot weaken analytical or risk gates. A high ranking score is never execution authorization.

## Exit and treasury handling

Realized altcoin proceeds return to USDT. The BNB treasury consumes only realized profit explicitly assigned to the vault and only when the separate BNB DCA guard passes. Profit availability alone never triggers a purchase.

## Non-goals

- No master-account trading
- No leverage, borrowing, shorting, or derivatives
- No autonomous withdrawals or internal transfers
- No silent retries
- No promise of profitability
