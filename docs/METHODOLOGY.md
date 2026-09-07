# Methodology

The agent uses aligned close-to-close returns from candles admitted by one decision time.

## BTC factor separation

Raw correlation is insufficient. The engine fits each candidate and BNB to BTC returns, then correlates their residual series. Low residual correlation means the broad market may explain the apparent relationship.

## Conditional beta

Upside beta uses observations where BNB is positive; downside beta uses negative observations. Attractive upside cannot override uncontrolled downside.

## Fail-closed gates

Correlation, residual correlation, upside beta, downside beta, liquidity, drawdown, and score must all pass. The weighted score is descriptive and cannot override a blocker.

## Limitations

Correlation is not causation; relationships decay; daily closes do not model fills; deterministic results prove behavior, not profitability; live MCP acquisition is read-only and host-injected in V1.
