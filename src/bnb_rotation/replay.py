from dataclasses import asdict, dataclass
from statistics import fmean

from .analytics import correlation, returns
from .pipeline import run_pipeline
from .research import diagnose_records, evaluate_split_experiment, evaluate_viability


@dataclass(frozen=True)
class ReplayMetrics:
    cumulative_return: float
    maximum_drawdown: float
    invested_periods: int
    total_periods: int


def _metrics(period_returns, invested_periods=0):
    equity = peak = 1.0
    drawdown = 0.0
    for value in period_returns:
        equity *= 1 + value
        peak = max(peak, equity)
        drawdown = max(drawdown, 1 - equity / peak)
    return ReplayMetrics(equity - 1, drawdown, invested_periods, len(period_returns))


def lead_lag_profile(asset, bnb, maximum_lag=3):
    """Correlation of BNB return at t with asset return at t + lag."""
    asset_returns, bnb_returns = returns(asset), returns(bnb)
    profile = {}
    for lag in range(maximum_lag + 1):
        left = bnb_returns[: len(bnb_returns) - lag or None]
        right = asset_returns[lag:]
        profile[str(lag)] = correlation(left, right)
    return profile


def walk_forward_replay(raw, decision_times, config, fee_rate=0.0):
    """Replay close-to-close returns using targets known at the prior close only."""
    symbols = [config["benchmark"], config["leader"], *config["candidates"]]
    by_close = {symbol: {c.close_time: c for c in raw[symbol]} for symbol in symbols}
    strategy_returns, bnb_returns, equal_weight_returns, usdt_returns = [], [], [], []
    records = []
    invested_periods = 0
    previous_allocations = {}

    for decision_time, next_time in zip(decision_times, decision_times[1:]):
        result = run_pipeline(raw, decision_time, config)
        if result["status"] != "READY":
            continue
        if any(next_time not in by_close[symbol] or decision_time not in by_close[symbol] for symbol in symbols):
            continue

        next_returns = {
            symbol: by_close[symbol][next_time].close / by_close[symbol][decision_time].close - 1
            for symbol in symbols
        }
        allocations = result["portfolio"]["allocations"]
        turnover = sum(
            abs(allocations.get(symbol, 0.0) - previous_allocations.get(symbol, 0.0))
            for symbol in set(allocations) | set(previous_allocations)
        )
        asset_contributions = {symbol: weight * next_returns[symbol] for symbol, weight in allocations.items()}
        transaction_cost = fee_rate * turnover
        strategy_return = sum(asset_contributions.values()) - transaction_cost
        if allocations:
            invested_periods += 1

        strategy_returns.append(strategy_return)
        bnb_returns.append(next_returns[config["leader"]])
        equal_weight_returns.append(fmean(next_returns[symbol] for symbol in config["candidates"]))
        usdt_returns.append(0.0)
        records.append({
            "decision_time": decision_time,
            "execution_period_end": next_time,
            "regime": result["bnb_regime"],
            "action": result["portfolio"]["action"],
            "allocations": allocations,
            "turnover": turnover,
            "transaction_cost": transaction_cost,
            "asset_contributions": asset_contributions,
            "bnb_return": next_returns[config["leader"]],
            "equal_weight_return": equal_weight_returns[-1],
            "strategy_return": strategy_return,
        })
        previous_allocations = allocations

    if not records:
        raise ValueError("NO_REPLAY_PERIODS")

    common = sorted(set.intersection(*(set(c.close_time for c in raw[s]) for s in symbols)))
    aligned = {s: [by_close[s][t] for t in common] for s in symbols}
    lead_lag = {
        symbol: lead_lag_profile(aligned[symbol], aligned[config["leader"]])
        for symbol in config["candidates"]
    }
    replay = {
        "method": "decision_at_t_applied_to_t_plus_1_close",
        "fee_rate": fee_rate,
        "periods": len(records),
        "strategy": asdict(_metrics(strategy_returns, invested_periods)),
        "benchmarks": {
            "bnb_hold": asdict(_metrics(bnb_returns, len(bnb_returns))),
            "equal_weight_candidates": asdict(_metrics(equal_weight_returns, len(equal_weight_returns))),
            "usdt_hold": asdict(_metrics(usdt_returns, 0)),
        },
        "lead_lag_correlations": lead_lag,
        "records": records,
    }
    replay["diagnostics"] = diagnose_records(records)
    replay["viability"] = evaluate_viability(replay, config["research_gate"])
    return replay


def chronological_split_replay(raw, decision_times, config, fee_rate=0.0):
    periods = len(decision_times) - 1
    train_end = int(periods * 0.60)
    validation_end = int(periods * 0.80)
    ranges = {
        "train": decision_times[: train_end + 1],
        "validation": decision_times[train_end : validation_end + 1],
        "holdout": decision_times[validation_end:],
    }
    splits = {name: walk_forward_replay(raw, times, config, fee_rate) for name, times in ranges.items()}
    return {
        "allocation": {name: replay["periods"] for name, replay in splits.items()},
        "splits": splits,
        "experiment_viability": evaluate_split_experiment(splits),
    }
