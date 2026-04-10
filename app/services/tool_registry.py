TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "fetch_ohlcv",
            "description": "Fetch historical OHLCV (candlestick) data for a trading symbol from Binance. Returns open, high, low, close, volume for each candle.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading symbol (e.g., 'BTC/USDT', 'ETH/USDT')",
                    },
                    "timeframe": {
                        "type": "string",
                        "description": "Candle timeframe (e.g., '1m', '5m', '1h', '1d')",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of candles to fetch (default 100, max 1000)",
                    },
                },
                "required": ["symbol", "timeframe"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compute_sharpe",
            "description": "Compute the Sharpe ratio from a list of returns. Assumes risk-free rate of 0. Higher values indicate better risk-adjusted returns.",
            "parameters": {
                "type": "object",
                "properties": {
                    "returns": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "List of periodic returns (as decimals, e.g., 0.01 for 1%)",
                    }
                },
                "required": ["returns"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compute_drawdown",
            "description": "Compute drawdown metrics from an equity curve. Returns maximum drawdown and drawdown series.",
            "parameters": {
                "type": "object",
                "properties": {
                    "equity_curve": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "List of equity values over time",
                    }
                },
                "required": ["equity_curve"],
            },
        },
    },
]


TOOL_MAP = {
    "fetch_ohlcv": "app.tools.market_data.fetch_ohlcv",
    "compute_sharpe": "app.tools.risk.compute_sharpe",
    "compute_drawdown": "app.tools.risk.compute_drawdown",
}
