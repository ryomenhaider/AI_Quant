import pandas as pd
import numpy as np
from typing import Any


def detect_spoofing(
    orderbook: dict, trades: list, metadata: dict, config: dict = None
) -> list[dict]:
    if config is None:
        config = {
            "size_threshold": 5.0,
            "lifetime_seconds": 2.0,
            "cancel_ratio_threshold": 0.8,
        }

    anomalies = []
    avg_order_size = metadata.get("avg_order_size", 1000)
    now = metadata.get("timestamp", 0)

    bids = orderbook.get("bids", [])
    asks = orderbook.get("asks", [])

    for side, orders in [("bid", bids), ("ask", asks)]:
        for level in orders:
            price = level.get("price", 0)
            size = level.get("size", 0)
            total_volume = level.get("total_volume", size)

            if size > avg_order_size * config["size_threshold"]:
                lifetime = level.get("lifetime_ms", 0) / 1000.0

                if lifetime < config["lifetime_seconds"]:
                    related_trades = _find_related_trades(
                        trades, price, side, window_pct=0.001
                    )

                    if related_trades:
                        trade_volume = sum(t.get("volume", 0) for t in related_trades)
                        cancel_ratio = 1 - (trade_volume / size)
                    else:
                        cancel_ratio = 1.0

                    if cancel_ratio >= config["cancel_ratio_threshold"]:
                        confidence = min(
                            1.0, (size / avg_order_size) / config["size_threshold"]
                        )

                        anomalies.append(
                            {
                                "type": "spoofing",
                                "confidence": round(confidence, 2),
                                "side": side,
                                "price_level": price,
                                "order_size": size,
                                "explanation": (
                                    f"Large {side} order of {size} placed at {price} "
                                    f"with lifetime {lifetime:.1f}s. "
                                    f"Near-zero execution suggests fake liquidity to move price. "
                                    f"This is typical spoofing behavior."
                                ),
                                "metrics": {
                                    "order_size": size,
                                    "avg_order_size": avg_order_size,
                                    "size_ratio": size / avg_order_size,
                                    "lifetime_seconds": lifetime,
                                    "cancel_ratio": cancel_ratio,
                                    "related_trade_volume": trade_volume
                                    if related_trades
                                    else 0,
                                },
                            }
                        )

    return anomalies


def _find_related_trades(
    trades: list, price: float, side: str, window_pct: float = 0.001
) -> list:
    related = []
    for trade in trades:
        trade_price = trade.get("price", 0)
        if abs(trade_price - price) / price < window_pct:
            related.append(trade)
    return related
