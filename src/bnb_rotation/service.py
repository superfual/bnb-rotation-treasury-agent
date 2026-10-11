"""Operator-reviewed research reports; no wallet, messaging or trading code."""
import copy
import hashlib
import json
import math
import re
from dataclasses import asdict
from datetime import datetime, timezone
from statistics import fmean

from .analytics import max_drawdown
from .binance import histories_from_snapshot
from .pipeline import run_pipeline

DAY = 86_400_000
SOURCE = "Binance MCP Server spot.klines"


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def utc(milliseconds):
    return datetime.fromtimestamp(milliseconds / 1000, timezone.utc).isoformat()


def validate_request(request):
    if not isinstance(request, dict):
        raise ValueError("request must be an object")
    allowed = {"request_id", "symbols", "time_horizon", "question", "weights"}
    if set(request) - allowed:
        raise ValueError("unknown request fields")
    symbols = request.get("symbols")
    if not isinstance(symbols, list) or not 1 <= len(symbols) <= 5:
        raise ValueError("request must contain one to five symbols")
    if any(not isinstance(s, str) or not re.fullmatch(r"[A-Z0-9]{2,20}USDT", s) for s in symbols):
        raise ValueError("symbols must be explicit uppercase Spot USDT pairs")
    if len(set(symbols)) != len(symbols):
        raise ValueError("duplicate requested symbols")
    for field in ("request_id", "time_horizon", "question"):
        value = request.get(field)
        if not isinstance(value, str) or not value.strip() or len(value) > 1000:
            raise ValueError(f"missing or invalid {field}")
    weights = request.get("weights")
    if weights is not None:
        if not isinstance(weights, dict) or set(weights) - set(symbols) - {"USDT"}:
            raise ValueError("weights must refer only to requested assets or USDT")
        if any(isinstance(w, bool) or not isinstance(w, (int, float)) or not math.isfinite(w) or not 0 <= w <= 1 for w in weights.values()):
            raise ValueError("weights must be finite fractions from zero to one")
        if abs(sum(weights.values()) - 1) > 1e-6:
            raise ValueError("portfolio weights must sum to one; include USDT reserve explicitly")
    return request


def admit_snapshot(snapshot, symbols, now_ms):
    if not isinstance(snapshot, dict) or not isinstance(snapshot.get("histories"), dict):
        raise ValueError("snapshot must contain symbol-keyed histories")
    if snapshot.get("source") != SOURCE or snapshot.get("mode") != "READ_ONLY":
        raise ValueError("untrusted snapshot metadata")
    if snapshot.get("market") != "SPOT" or snapshot.get("interval") != "1d":
        raise ValueError("report requires UTC daily Spot candles")
    decision = snapshot.get("decision_time_utc_ms")
    if isinstance(decision, bool) or not isinstance(decision, int) or not 0 <= now_ms - decision <= 900_000:
        raise ValueError("snapshot collection time is future or older than fifteen minutes")
    histories = histories_from_snapshot(snapshot)
    admitted = {}
    latest_expected = decision // DAY * DAY - 1
    for symbol in symbols:
        if symbol not in histories:
            raise ValueError(f"missing data: {symbol}")
        closed = [c for c in histories[symbol] if c.close_time <= decision and c.open_time <= decision]
        if len(closed) < 120:
            raise ValueError(f"insufficient closed daily candles: {symbol}")
        times = [c.open_time for c in closed]
        if any(b - a != DAY for a, b in zip(times, times[1:])):
            raise ValueError(f"unordered, duplicate or missing daily candles: {symbol}")
        for c in closed:
            values = (c.open, c.high, c.low, c.close, c.volume, c.quote_volume)
            if not all(math.isfinite(v) for v in values):
                raise ValueError(f"non-finite OHLCV: {symbol}")
            if min(values[:4]) <= 0 or min(values[4:]) < 0 or not c.low <= min(c.open, c.close) <= max(c.open, c.close) <= c.high:
                raise ValueError(f"invalid OHLCV: {symbol}")
            if c.open_time % DAY or c.close_time != c.open_time + DAY - 1:
                raise ValueError(f"wrong UTC daily interval: {symbol}")
        if closed[-1].close_time != latest_expected:
            raise ValueError(f"stale latest closed daily candle: {symbol}")
        admitted[symbol] = closed[-120:]
    timelines = {tuple(c.open_time for c in rows) for rows in admitted.values()}
    if len(timelines) != 1:
        raise ValueError("requested assets and benchmarks are not aligned")
    return admitted


def build_report(snapshot, request, config, now_ms):
    validate_request(request)
    candidates = [s for s in request["symbols"] if s not in (config["benchmark"], config["leader"])]
    required = list(dict.fromkeys([config["benchmark"], config["leader"], *request["symbols"]]))
    histories = admit_snapshot(snapshot, required, now_ms)
    custom = copy.deepcopy(config)
    custom["candidates"] = candidates
    custom["history"]["minimum_closed_candles"] = 120
    result = run_pipeline(histories, snapshot["decision_time_utc_ms"], custom)
    if result["status"] != "READY":
        raise ValueError(f"analysis blocked: {result['reason']}")
    assets = []
    for symbol in request["symbols"]:
        candles = histories[symbol]
        last = candles[-1].close
        assets.append({"symbol": symbol, "last_closed_price": last,
                       "return_7d": last / candles[-8].close - 1,
                       "return_30d": last / candles[-31].close - 1,
                       "sma20": fmean(c.close for c in candles[-20:]),
                       "sma50": fmean(c.close for c in candles[-50:]),
                       "maximum_drawdown_120d": max_drawdown(candles),
                       "average_daily_quote_volume_20d_usdt": fmean(c.quote_volume for c in candles[-20:])})
    weights = request.get("weights")
    portfolio = None
    if weights is not None:
        concentration = {s: w for s, w in weights.items() if s != "USDT" and w > config["portfolio"]["maximum_weight"]}
        reserve = weights.get("USDT", 0)
        portfolio = {"supplied_weights": weights, "above_configured_weight_limit": concentration,
                     "configured_maximum_asset_weight": config["portfolio"]["maximum_weight"],
                     "usdt_reserve": reserve, "below_configured_reserve_floor": reserve < config["portfolio"]["minimum_usdt_reserve"]}
    return {"schema_version": 1, "status": "DRAFT_REQUIRES_OPERATOR_REVIEW",
            "request": request, "generated_at_utc": utc(now_ms),
            "data": {"source": SOURCE, "market": "SPOT", "interval": "1d", "candles_per_symbol": 120,
                     "latest_closed_candle_utc": utc(histories[config["leader"]][-1].close_time),
                     "snapshot_sha256": fingerprint(snapshot), "config_sha256": fingerprint(config)},
            "analysis": {"bnb_regime": result["bnb_regime"], "regime_blockers": list(result["regime_blockers"]),
                         "shock_blockers": list(result["shock_blockers"]), "assets": assets,
                         "ranking": [asdict(r) for r in result["ranking"]], "portfolio_risk": portfolio,
                         "paper_scenario": result["portfolio"]},
            "limitations": ["Research draft only; the operator must review before delivery.",
                            "Daily Spot OHLCV is not on-chain liquidity, slippage or contract-risk verification.",
                            "Ranking covers only requested candidates, not the whole BNB ecosystem.",
                            "Correlation and BTC residuals do not establish causation or future returns.",
                            "The historical strategy failed live-readiness gates; this report does not change that result.",
                            "Paper allocation is a model scenario, not an order or authorization to trade.",
                            "No wallet access, autonomous execution, automatic quote, payment confirmation or delivery is performed."]}


def render_markdown(report):
    a = report["analysis"]
    lines = ["# Fual Treasury — portfolio research draft", "", "**Operator review required before delivery.**", "",
             f"Request: {report['request']['request_id']}", f"Research question: {report['request']['question']}",
             f"Client horizon: {report['request']['time_horizon']}", "",
             f"Data: Binance Spot, daily, 120 closed candles per symbol. Latest close: {report['data']['latest_closed_candle_utc']}.",
             f"Generated: {report['generated_at_utc']}", "", f"BNB regime: **{a['bnb_regime']}**",
             "Regime blockers: " + (", ".join(a["regime_blockers"]) or "none"),
             "Shock blockers: " + (", ".join(a["shock_blockers"]) or "none"), "", "## Asset observations", "",
             "| Asset | Closed price | 7d return | 30d return | SMA20 | SMA50 | 120d drawdown | Avg 20d daily quote volume |",
             "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for x in a["assets"]:
        lines.append(f"| {x['symbol']} | {x['last_closed_price']:.6g} | {x['return_7d']:.2%} | {x['return_30d']:.2%} | {x['sma20']:.6g} | {x['sma50']:.6g} | {x['maximum_drawdown_120d']:.2%} | {x['average_daily_quote_volume_20d_usdt']:,.0f} USDT |")
    lines += ["", "## BNB-relative ranking", "", "| Asset | Score | BTC-adjusted correlation | Result | Failed gates |", "|---|---:|---:|---|---|"]
    for x in a["ranking"]:
        lines.append(f"| {x['symbol']} | {x['score']:.2f} | {x['residual_correlation']:.3f} | {x['decision']} | {', '.join(x['blockers']) or 'none'} |")
    lines += ["", "## Portfolio risk", ""]
    p = a["portfolio_risk"]
    if p is None:
        lines += ["No portfolio weights supplied. Concentration and reserve checks cannot be calculated."]
    else:
        lines += [f"Supplied USDT reserve: {p['usdt_reserve']:.1%}; configured floor: 20%.",
                  f"Below reserve floor: {p['below_configured_reserve_floor']}.",
                  "Assets above the configured 20% weight limit: " + (", ".join(f"{s} ({w:.1%})" for s, w in p["above_configured_weight_limit"].items()) or "none")]
    lines += ["", "## Conditional model scenario", "", f"Current paper result: **{a['paper_scenario']['action']}**.",
              "A rotation scenario requires BNB above SMA20, positive ten-day mean returns, BTC above SMA50, passing candidate gates and no shock blockers. Loss of any required gate invalidates it.",
              "This daily model does not provide intraday entry, stop-loss or take-profit levels. The client's question and horizon still require operator interpretation.",
              "", "## Limitations", ""]
    lines += [f"- {item}" for item in report["limitations"]]
    lines += ["", "Snapshot SHA-256: " + report["data"]["snapshot_sha256"], "Config SHA-256: " + report["data"]["config_sha256"], ""]
    return "\n".join(lines)
