# Live evidence

- Source: Binance MCP Server `spot.klines`
- Mode: read-only market data
- Decision time: `1788807042450` UTC-ms
- Universe: BTCUSDT, BNBUSDT, and 16 configured candidates
- Requested: 500 daily candles per symbol
- Admitted for replay: 499 aligned, closed candles per symbol
- Rolling analysis lookback: maximum 120 closed candles
- Snapshot SHA-256: `263a6c59216bd8888be2eec45ec5bfa50a59f627f0d018dd407d37828822bcdb`

## Result

- BNB regime: `RISK_ON`
- Fully qualified relationship candidate: `CAKEUSDT`
- CAKE score: `71.3`
- CAKE raw BNB correlation: `0.80`
- CAKE BTC-adjusted residual correlation: `0.64`
- CAKE upside beta: `1.21`
- CAKE downside beta: `1.15`
- Paper portfolio: `ROTATION_READY`
- BNB profit vault: `HOLD_USDT`

The result is analytical and paper-only. It is not an instruction or authorization to buy CAKE, and the snapshot contains no account information or credentials.

## Multi-regime replay

The same snapshot provides 409 out-of-sample daily periods from 2025-07-24 through 2026-09-06. The paper strategy returned -13.91% with 21.90% maximum drawdown, versus BNB hold at -2.30% / 58.20%, equal-weight candidates at -49.52% / 74.00%, and USDT at 0%. The strategy reduced drawdown but did not beat BNB or USDT, so the research gate remains failed and live deployment is not justified.
