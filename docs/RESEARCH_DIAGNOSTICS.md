# Research diagnostics

## Gate result

`FAILED_NOT_LIVE_READY`

The 409-period Binance MCP walk-forward replay failed two conjunctive requirements:

- `STRATEGY_RETURN_BELOW_FLOOR`: strategy return was -13.91%, below the 0% floor.
- `UNDERPERFORMS_BNB`: strategy return trailed BNB hold by 11.61 percentage points.

It passed the sample-size, invested-period, and 25% maximum-drawdown requirements. Passing individual safety checks cannot override either failed return check.

## Loss attribution

- Invested periods: 86; 36 positive and 50 negative.
- Average gross exposure across all periods: 12.47%.
- Estimated transaction cost: 1.62% of initial equity in additive period terms; this is material but not the primary explanation for the loss.
- Largest negative gross contributors: ETH (-3.57%), SOL (-2.77%), AVAX (-2.44%), LINK (-2.40%), DOGE (-1.05%), UNI (-1.01%), and CAKE (-1.00%).
- Positive gross contributors: NEAR (+1.56%), AAVE (+0.70%), and INJ (+0.52%).

The five worst next-day paper periods began on 2025-10-09 (-4.74%), 2025-08-18 (-4.51%), 2025-08-13 (-4.43%), 2025-09-21 (-4.24%), and 2025-07-31 (-3.24%). Four included CAKE and several clustered ETH/SOL/LINK exposure. The evidence suggests that relationship qualification alone did not protect against abrupt next-day reversals during nominally risk-on conditions.

## Research discipline

No thresholds are changed from this result. Tuning them on the same evaluation window would contaminate the evidence. The next experiment must introduce a pre-declared shock/exit hypothesis, freeze its parameters, and evaluate it on separated train, validation, and holdout windows.
