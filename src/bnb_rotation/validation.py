from .models import Candle

class DataValidationError(ValueError):
    pass

def closed_history(candles: list[Candle], decision_time: int, minimum: int, maximum_age_seconds: int) -> list[Candle]:
    admitted = [c for c in candles if c.open_time <= decision_time and c.close_time <= decision_time]
    if len(admitted) < minimum:
        raise DataValidationError(f"insufficient closed history: {len(admitted)} < {minimum}")
    times = [c.open_time for c in admitted]
    if len(times) != len(set(times)) or any(a >= b for a, b in zip(times, times[1:])):
        raise DataValidationError("history must be unique and strictly ordered")
    if any(c.close_time <= c.open_time for c in admitted):
        raise DataValidationError("invalid candle interval")
    if decision_time - admitted[-1].close_time > maximum_age_seconds * 1000:
        raise DataValidationError("latest closed candle is stale")
    return admitted

def align_histories(histories: dict[str, list[Candle]]) -> dict[str, list[Candle]]:
    common = set.intersection(*(set(c.open_time for c in candles) for candles in histories.values()))
    if len(common) < 2:
        raise DataValidationError("insufficient aligned history")
    ordered = sorted(common)
    return {symbol: [next(c for c in candles if c.open_time == t) for t in ordered] for symbol, candles in histories.items()}
