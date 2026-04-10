import numpy as np


def compute_sharpe(returns: list[float]) -> dict:
    try:
        if not returns:
            return {"status": "error", "data": None, "error": "Empty returns list"}

        arr = np.array(returns)
        std = np.std(arr)

        if std == 0:
            sharpe = 0.0
        else:
            sharpe = float(np.mean(arr) / std)

        return {"status": "success", "data": {"sharpe_ratio": sharpe}, "error": None}
    except Exception as e:
        return {"status": "error", "data": None, "error": str(e)}


def compute_drawdown(equity_curve: list[float]) -> dict:
    try:
        if not equity_curve:
            return {"status": "error", "data": None, "error": "Empty equity curve"}

        arr = np.array(equity_curve)
        running_max = np.maximum.accumulate(arr)
        drawdown = (arr - running_max) / running_max

        max_dd = float(np.min(drawdown))

        return {
            "status": "success",
            "data": {"max_drawdown": max_dd, "drawdown_series": drawdown.tolist()},
            "error": None,
        }
    except Exception as e:
        return {"status": "error", "data": None, "error": str(e)}
