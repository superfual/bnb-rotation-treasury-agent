# Experiment 001 — closed-candle shock and extension filter

## Pre-registered hypothesis

The relationship gates are slow-moving and can remain qualified immediately before an abrupt next-day reversal. A short-horizon, closed-candle filter may reject fragile entries without using intraday or future information.

Parameters are fixed before evaluating the chronological holdout:

- block all rotation if the latest closed BNB daily return is at or below -3%;
- block all rotation if the latest closed BTC daily return is at or below -3%;
- block all rotation if BNB closes below 35% of its own daily high-low range;
- block an individual candidate if its latest closed daily return is at or above +8%.

The 409 replay periods are split chronologically into 60% train, 20% validation, and 20% untouched holdout. The experiment is descriptive: these thresholds will not be changed after seeing holdout results.

Success is not defined as a single profitable window. Report return, maximum drawdown, exposure, and blockers for every split, then retain the existing full-sample research viability gate.

## Frozen evaluation result

The thresholds above were not changed after opening the splits.

| Split | Periods | Strategy | Max drawdown | BNB hold | Invested periods |
|---|---:|---:|---:|---:|---:|
| Train | 245 | +4.66% | 8.61% | -18.41% | 25 |
| Validation | 82 | -7.11% | 8.80% | -3.80% | 20 |
| Holdout | 82 | +3.18% | 0.55% | +24.48% | 9 |

Experiment status: `FAILED_NOT_LIVE_READY`.

Blockers: `VALIDATION_RETURN_BELOW_FLOOR`, `VALIDATION_UNDERPERFORMS_BNB`, and `HOLDOUT_UNDERPERFORMS_BNB`. The full 409-period sample improved to +0.32% with 10.81% maximum drawdown, but that aggregate pass does not override the independent validation and holdout failures.
