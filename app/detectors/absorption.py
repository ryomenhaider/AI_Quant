import numpy as np
from typing import Any


def detect_absorption(
    orderbook: dict, trades: list, metadata: dict, config: dict = None
) -> list[dict]:
    if config is None:
        config = {
            "volume_threshold": 10000,
            "price_change_threshold": 0.002,
            "repeated_fills": 3,
        }

    anomalies = []

    if not trades or not orderbook:
        return anomalies

    mid_price = _get_mid_price(orderbook)
    current_price = metadata.get("last_price", mid_price)

    bids = orderbook.get("bids", [])
    asks = orderbook.get("asks", [])

    price_levels = {}
    for level in bids + asks:
        price = level.get("price", 0)
        size = level.get("size", 0)
        price_levels[price] = size

    for i, trade in enumerate(trades):
        trade_price = trade.get("price", 0)
        trade_volume = trade.get("volume", 0)
        trade_side = trade.get("side", "unknown")

        if trade_volume < config["volume_threshold"]:
            continue

        relevant_levels = _get_nearest_levels(trade_price, price_levels, n=3)

        volume_at_levels = sum(price_levels.get(p, 0) for p in relevant_levels)

        future_trades = trades[i + 1 : i + 1 + config["repeated_fills"]]
        future_volume = sum(t.get("volume", 0) for t in future_trades)

        price_change = (
            abs(trade_price - current_price) / current_price if current_price > 0 else 0
        )

        if (
            volume_at_levels > config["volume_threshold"] * 2
            and price_change < config["price_change_threshold"]
            and trade_volume > config["volume_threshold"]
        ):
            confidence = min(1.0, volume_at_levels / (config["volume_threshold"] * 5))

            anomalies.append(
                {
                    "type": "absorption",
                    "confidence": round(confidence, 2),
                    "side": trade_side,
                    "price_level": trade_price,
                    "explanation": (
                        f"Large {trade_side} trade of {trade_volume} at {trade_price}. "
                        f"Volume absorbed: {volume_at_levels:.0f} at nearby levels. "
                        f"Price moved only {price_change * 100:.2f}%. "
                        f"This indicates liquidity absorption - large orders are being filled "
                        f"against resting liquidity without moving price."
                    ),
                    "metrics": {
                        "trade_volume": trade_volume,
                        "volume_at_levels": volume_at_levels,
                        "price_change_pct": price_change * 100,
                        "repeated_fills": len(future_trades),
                        "future_volume": future_volume,
                    },
                }
            )

    return anomalies


def _get_mid_price(orderbook: dict) -> float:
    bids = orderbook.get("bids", [])
    asks = orderbook.get("asks", [])

    best_bid = bids[0].get("price", 0) if bids else 0
    best_ask = asks[0].get("price", 0) if asks else 0

    if best_bid and best_ask:
        return (best_bid + best_ask) / 2
    return best_ask or best_bid or 0


def _get_nearest_levels(price: float, price_levels: dict, n: int = 3) -> list:
    sorted_prices = sorted(price_levels.keys())
    nearest = []

    for p in sorted_prices:
        if len(nearest) >= n:
            break
        nearest.append(p)

    return nearest[:n]
