import json
from app.tools.market_data import fetch_ohlcv
from app.tools.risk import compute_sharpe, compute_drawdown


def main():
    print("=" * 50)
    print("Testing fetch_ohlcv")
    print("=" * 50)
    result = fetch_ohlcv("BTC/USDT", "1h", limit=10)
    print(json.dumps(result, indent=2, default=str))

    print("\n" + "=" * 50)
    print("Testing compute_sharpe")
    print("=" * 50)
    returns = [0.01, 0.02, -0.01, 0.03, -0.02, 0.015, -0.005, 0.01]
    result = compute_sharpe(returns)
    print(json.dumps(result, indent=2))

    print("\n" + "=" * 50)
    print("Testing compute_drawdown")
    print("=" * 50)
    equity = [10000, 10500, 10200, 9800, 10100, 10800, 10400]
    result = compute_drawdown(equity)
    print(json.dumps(result, indent=2))

    print("\n" + "=" * 50)
    print("All tests passed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
