from .models import Candle

def candle_from_binance(row):
    if len(row) < 11:
        raise ValueError("invalid Binance kline row")
    return Candle(
        open_time=int(row[0]), close_time=int(row[6]),
        open=float(row[1]), high=float(row[2]), low=float(row[3]), close=float(row[4]),
        volume=float(row[5]), quote_volume=float(row[7]),
    )

def histories_from_snapshot(snapshot):
    if snapshot.get("source") != "Binance MCP Server spot.klines" or snapshot.get("mode") != "READ_ONLY":
        raise ValueError("untrusted snapshot metadata")
    return {symbol:[candle_from_binance(row) for row in rows] for symbol,rows in snapshot["histories"].items()}
