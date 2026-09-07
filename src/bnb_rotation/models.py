from dataclasses import dataclass

@dataclass(frozen=True)
class Candle:
    open_time: int
    close_time: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    quote_volume: float

@dataclass(frozen=True)
class Relationship:
    symbol: str
    correlation: float
    stability: float
    upside_beta: float
    downside_beta: float
    residual_correlation: float
    relative_strength: float
    max_drawdown: float
    average_quote_volume: float
    score: float
    decision: str
    blockers: tuple[str, ...]
