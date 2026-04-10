import pandas as pd
import numpy as np

from app.tools.market_data import fetch_ohlcv
from app.strategies.moving_average import generate_signals as ma_signals
from app.strategies.breakout import generate_signals as breakout_signals


STRATEGY_REGISTRY = {
    "moving_average_crossover": ma_signals,
    "breakout": breakout_signals,
}

VALID_PARAMS = {
    "moving_average_crossover": ["fast_window", "slow_window"],
    "breakout": ["window"],
}


def run_backtest(
    symbol: str, timeframe: str, strategy: str, params: dict, limit: int = 500
) -> dict:
    try:
        if strategy not in STRATEGY_REGISTRY:
            return {
                "status": "error",
                "data": None,
                "error": f"Unknown strategy: {strategy}. Valid strategies: {list(STRATEGY_REGISTRY.keys())}",
            }

        data_result = fetch_ohlcv(symbol, timeframe, limit)
        if data_result["status"] != "success":
            return data_result

        candles = data_result["data"]["candles"]
        if len(candles) < 100:
            return {
                "status": "error",
                "data": None,
                "error": "Insufficient data for backtest",
            }

        df = pd.DataFrame(candles)
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = pd.to_numeric(df[col])

        strategy_func = STRATEGY_REGISTRY[strategy]
        param_keys = VALID_PARAMS.get(strategy, [])

        invalid_keys = set(params.keys()) - set(param_keys)
        if invalid_keys:
            return {
                "status": "error",
                "data": None,
                "error": f"Invalid params for {strategy}: {invalid_keys}",
            }

        signal_params = {k: v for k, v in params.items() if k in param_keys}
        entries = strategy_func(df, **signal_params)

        try:
            import vectorbt as vbt
        except ImportError:
            return {"status": "error", "data": None, "error": "vectorbt not available"}

        close = df["close"].values
        portfolio = vbt.Portfolio.from_signals(
            close, entries=entries, exits=None, size=1.0, fees=0.001, slippage=0.001
        )

        returns = portfolio.returns()
        returns_arr = returns.values.flatten()
        pnl = float(np.nansum(returns_arr)) * 100

        std_val = np.nanstd(returns_arr)
        mean_val = np.nanmean(returns_arr)
        sharpe = float(mean_val / std_val * np.sqrt(365 * 24)) if std_val > 0 else 0.0

        equity = portfolio.value()
        equity_arr = equity.values.flatten()
        running_max = np.maximum.accumulate(equity_arr)
        drawdown_arr = (equity_arr - running_max) / running_max
        max_dd = float(np.nanmin(drawdown_arr)) * 100

        num_trades = int(portfolio.trades.count())

        return {
            "status": "success",
            "data": {
                "symbol": symbol,
                "strategy": strategy,
                "params": params,
                "pnl": round(pnl, 2),
                "sharpe": round(sharpe, 2),
                "max_drawdown": round(max_dd, 2),
                "trades": num_trades,
            },
            "error": None,
        }

    except Exception as e:
        return {"status": "error", "data": None, "error": str(e)}
