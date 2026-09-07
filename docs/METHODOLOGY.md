# Methodology

## Walk-forward chronology

For a decision time `t`, the engine admits only candles whose close time is at or before `t` and keeps at most the latest 120. The resulting target allocation is applied to the next observed close-to-close return, `t → t+1`. All benchmarks use the identical period. Future mutations and observations before the rolling lookback therefore cannot alter the decision.

Trading cost is approximated as 10 bps multiplied by the absolute change in target asset weights. Unchanged allocations have zero turnover cost. Slippage, spread, tax, and market impact are not modeled.

Lead/lag diagnostics report the correlation between BNB return at `t` and candidate return at `t + lag` for lags zero through three. They are descriptive diagnostics and are not treated as proof that BNB causes a later altcoin move.

## Research viability gate

The replay is not live-ready unless every pre-declared gate passes: at least 252 periods, at least 20 invested periods, non-negative strategy return, return no lower than BNB hold, and maximum drawdown no greater than 25%. The gate is conjunctive; lower drawdown cannot compensate for failed return requirements.

The agent uses aligned close-to-close returns from candles admitted by one decision time.

## BTC factor separation

Raw correlation is insufficient. The engine fits each candidate and BNB to BTC returns, then correlates their residual series. Low residual correlation means the broad market may explain the apparent relationship.

## Conditional beta

Upside beta uses observations where BNB is positive; downside beta uses negative observations. Attractive upside cannot override uncontrolled downside.

## Fail-closed gates

Correlation, residual correlation, upside beta, downside beta, liquidity, drawdown, and score must all pass. The weighted score is descriptive and cannot override a blocker.

## Limitations

Correlation is not causation; relationships decay; daily closes do not model fills; deterministic results prove behavior, not profitability; live MCP acquisition is read-only and host-injected in V1.
