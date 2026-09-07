# Track A submission package

## Recommended video title

**BNB Rotation Agent: When AI Refuses to Trade | Binance Agent OS**

## 90-second voice-over

### 00:00–00:15

This is the BNB Rotation and Treasury Agent, a paper-trading workflow built with Binance Agent OS and Binance MCP market data.

### 00:15–00:30

It detects BNB risk-on conditions, then ranks liquid Spot altcoins by BNB sensitivity after removing the common Bitcoin factor.

### 00:30–00:45

Every decision uses closed candles only. Missing history, market shocks, excessive extension, or failed risk checks immediately blocks rotation.

### 00:45–01:00

We tested 409 out-of-sample periods. A pre-registered shock filter improved full-sample drawdown from twenty-two percent to eleven percent.

### 01:00–01:15

But validation lost money, and holdout underperformed BNB. Therefore, the independent research gate rejected live execution—even with a current qualified candidate.

### 01:15–01:30

Judges can reproduce the pipeline in GitHub Actions. Binance MCP evidence, no-look-ahead tests, frozen thresholds, and green CI support every claim.

## Screen-recording shot list

| Time | Screen | Action |
|---|---|---|
| 00:00–00:12 | GitHub Pages dashboard | Show the project name and `PAPER ONLY · FAIL CLOSED` badge. |
| 00:12–00:27 | Live snapshot panel | Point to BNB `RISK_ON`, CAKE qualification, and the closed-candle evidence hash. |
| 00:27–00:42 | Decision pipeline | Follow Binance MCP → closed candles → BTC filter → BNB regime → risk gates → paper treasury. |
| 00:42–00:58 | Experiment 001 panel | Show the 409-period full sample and drawdown improvement. |
| 00:58–01:13 | Frozen split results | Show validation -7.11%, holdout +3.18%, and holdout BNB +24.48%. |
| 01:13–01:25 | GitHub Actions | Open `Control-Room Demo`, job `demo`, then expand `Show verified Binance MCP evidence`. |
| 01:25–01:30 | Final log lines | Hold on `FAILED_NOT_LIVE_READY` and `PAPER RESEARCH ONLY — NO LIVE EXECUTION`. |

## Public links

- Dashboard: https://superfual.github.io/bnb-rotation-treasury-agent/
- Repository: https://github.com/superfual/bnb-rotation-treasury-agent
- Control-Room Demo: https://github.com/superfual/bnb-rotation-treasury-agent/actions/workflows/control-room-demo.yml

## X submission draft

🛠️ Track A — BNB Rotation & Treasury Agent

Uses Binance MCP to rank BNB-sensitive Spot altcoins, then validates decisions with closed-candle, no-look-ahead replay. Its independent holdout gate failed, so the agent refused live execution.

Dashboard: https://superfual.github.io/bnb-rotation-treasury-agent/

GitHub: https://github.com/superfual/bnb-rotation-treasury-agent

Video: [ADD PUBLIC VIDEO LINK]

## Survey project description

BNB Rotation & Treasury Agent is a defensive Binance Agent OS workflow for BNB holders. Using read-only Binance MCP Spot data, it detects BNB-led risk-on regimes and ranks liquid altcoins through correlation stability, conditional upside and downside beta, liquidity, drawdown, relative strength, and BTC-adjusted residual correlation. Every decision uses a single UTC time and closed candles only. A conjunctive risk pipeline can hold USDT even when individual candidates rank highly. The project includes a 409-period walk-forward replay, frozen chronological train/validation/holdout evaluation, transaction-cost approximation, loss attribution, automated no-look-ahead tests, a GitHub Actions control-room demo, and a public dashboard. Experiment 001 improved full-sample drawdown but failed validation and BNB-relative holdout requirements, so the agent correctly remained paper-only and rejected live deployment.

## Replication guide

1. Clone the public repository and use Python 3.11 or newer.
2. Run `PYTHONPATH=src python -m unittest discover -s tests -v`.
3. Run `python scripts/run_demo.py` for the deterministic decision pipeline.
4. Run `python scripts/run_replay.py` for deterministic walk-forward comparison.
5. Run `python scripts/show_evidence.py` for the verified Binance MCP evidence report.
6. Alternatively, open GitHub Actions → Control-Room Demo → Run workflow on `main`.
7. Inspect the final experiment gate and blockers. No exchange credentials are required, and the V1 repository contains no real-order adapter.
