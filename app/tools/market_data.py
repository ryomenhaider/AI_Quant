import ccxt
import pandas as pd

from app.utils.serializers import dataframe_to_dict


def fetch_ohlcv(symbol: str, timeframe: str, limit: int = 100) -> dict:
    try:
        exchange = ccxt.binance()
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

        df = pd.DataFrame(
            ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
        )
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

        return {
            "status": "success",
            "data": {
                "symbol": symbol,
                "timeframe": timeframe,
                "candles": dataframe_to_dict(df),
            },
            "error": None,
        }
    except Exception as e:
        return {"status": "error", "data": None, "error": str(e)}
