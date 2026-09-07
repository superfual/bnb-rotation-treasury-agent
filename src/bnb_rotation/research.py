from collections import Counter, defaultdict


def evaluate_viability(replay, limits):
    strategy = replay["strategy"]
    bnb = replay["benchmarks"]["bnb_hold"]
    checks = (
        (replay["periods"] >= limits["minimum_periods"], "INSUFFICIENT_REPLAY_PERIODS"),
        (strategy["invested_periods"] >= limits["minimum_invested_periods"], "INSUFFICIENT_INVESTED_PERIODS"),
        (strategy["cumulative_return"] >= limits["minimum_strategy_return"], "STRATEGY_RETURN_BELOW_FLOOR"),
        (
            strategy["cumulative_return"] - bnb["cumulative_return"] >= limits["minimum_excess_return_vs_bnb"],
            "UNDERPERFORMS_BNB",
        ),
        (strategy["maximum_drawdown"] <= limits["maximum_strategy_drawdown"], "DRAWDOWN_EXCEEDS_LIMIT"),
    )
    blockers = [reason for passed, reason in checks if not passed]
    return {
        "status": "PASSED_PAPER_RESEARCH" if not blockers else "FAILED_NOT_LIVE_READY",
        "blockers": blockers,
        "observations": {
            "strategy_return": strategy["cumulative_return"],
            "excess_return_vs_bnb": strategy["cumulative_return"] - bnb["cumulative_return"],
            "strategy_maximum_drawdown": strategy["maximum_drawdown"],
        },
    }


def diagnose_records(records, worst_count=5):
    contribution = defaultdict(float)
    action_counts = Counter()
    total_cost = 0.0
    invested_exposure = 0.0
    for record in records:
        action_counts[record["action"]] += 1
        total_cost += record["transaction_cost"]
        invested_exposure += sum(record["allocations"].values())
        for symbol, value in record["asset_contributions"].items():
            contribution[symbol] += value
    invested = [r for r in records if r["allocations"]]
    return {
        "action_counts": dict(sorted(action_counts.items())),
        "winning_invested_periods": sum(r["strategy_return"] > 0 for r in invested),
        "losing_invested_periods": sum(r["strategy_return"] < 0 for r in invested),
        "average_gross_exposure": invested_exposure / len(records),
        "total_transaction_cost": total_cost,
        "gross_contribution_by_symbol": dict(sorted(contribution.items(), key=lambda item: item[1])),
        "worst_periods": sorted(
            (
                {
                    "decision_time": r["decision_time"],
                    "execution_period_end": r["execution_period_end"],
                    "strategy_return": r["strategy_return"],
                    "allocations": r["allocations"],
                }
                for r in records
            ),
            key=lambda r: r["strategy_return"],
        )[:worst_count],
    }


def evaluate_split_experiment(splits):
    blockers = []
    for name in ("validation", "holdout"):
        replay = splits[name]
        strategy_return = replay["strategy"]["cumulative_return"]
        bnb_return = replay["benchmarks"]["bnb_hold"]["cumulative_return"]
        if strategy_return < 0:
            blockers.append(f"{name.upper()}_RETURN_BELOW_FLOOR")
        if strategy_return < bnb_return:
            blockers.append(f"{name.upper()}_UNDERPERFORMS_BNB")
    return {
        "status": "PASSED_PAPER_EXPERIMENT" if not blockers else "FAILED_NOT_LIVE_READY",
        "blockers": blockers,
    }
