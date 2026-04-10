import json
from app.tools.anomaly import detect_anomaly


def main():
    print("=" * 50)
    print("Testing detect_anomaly")
    print("=" * 50)

    orderbook = {
        "bids": [
            {"price": 50000, "size": 5000, "total_volume": 5000, "lifetime_ms": 500},
            {"price": 49900, "size": 1000, "total_volume": 1000, "lifetime_ms": 5000},
        ],
        "asks": [
            {"price": 50100, "size": 30000, "total_volume": 30000, "lifetime_ms": 800},
            {"price": 50200, "size": 2000, "total_volume": 2000, "lifetime_ms": 10000},
        ],
    }

    trades = [
        {"price": 50000, "volume": 100, "side": "buy"},
        {"price": 50050, "volume": 150, "side": "buy"},
        {"price": 50100, "volume": 500, "side": "sell"},
        {"price": 50100, "volume": 600, "side": "sell"},
    ]

    metadata = {
        "avg_order_size": 5000,
        "avg_trade_size": 200,
        "timestamp": 1700000000000,
        "last_price": 50100,
    }

    result = detect_anomaly(orderbook, trades, metadata)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
