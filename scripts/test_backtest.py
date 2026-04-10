import json
from app.tools.backtest import run_backtest


def main():
    print("=" * 50)
    print("Testing run_backtest")
    print("=" * 50)

    result = run_backtest(
        symbol="BTC/USDT",
        timeframe="1h",
        strategy="moving_average_crossover",
        params={"fast_window": 10, "slow_window": 50},
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
