import numpy as np
from typing import Any


def detect_aggressive_flow(
    orderbook: dict, trades: list, metadata: dict, config: dict = None
) -> list[dict]:
    if config is None:
        config = {
            "size_multiplier": 3.0,
            "imbalance_threshold": 0.7,
        }

    anomalies = []

    if not trades:
        return anomalies

    avg_trade_size = metadata.get("avg_trade_size", 1000)
    buy_volume = 0.0
    sell_volume = 0.0

    for trade in trades:
        side = trade.get("side", "buy")
        volume = trade.get("volume", 0)

        if side.lower() in ("buy", "bid", "ask", "sell"):
            if side.lower() in ("buy", "bid"):
                buy_volume += volume
            else:
                sell_volume += volume

    total_volume = buy_volume + sell_volume
    if total_volume == 0:
        return anomalies

    buy_ratio = buy_volume / total_volume
    sell_ratio = sell_volume / total_volume

    buy_imbalance = abs(buy_ratio - 0.5) * 2
    sell_imbalance = abs(sell_ratio - 0.5) * 2

    if buy_imbalance > config["imbalance_threshold"]:
        dominant_side = "buy"
        ratio = buy_ratio
    elif sell_imbalance > config["imbalance_threshold"]:
        dominant_side = "sell"
        ratio = sell_ratio
    else:
        return anomalies

    spikes = [
        t
        for t in trades
        if t.get("volume", 0) > avg_trade_size * config["size_multiplier"]
    ]

    if spikes:
        largest_spike = max(spikes, key=lambda x: x.get("volume", 0))

        confidence = min(1.0, len(spikes) / 5) * buy_imbalance

        anomalies.append(
            {
                "type": "aggressive_flow",
                "confidence": round(confidence, 2),
                "side": dominant_side,
                "price_level": largest_spike.get("price", 0),
                "explanation": (
                    f"One-sided aggressive {dominant_side} flow detected. "
                    f"Buy/Sell ratio: {buy_ratio:.1%}/{sell_ratio:.1%}. "
                    f"{len(spikes)} large orders (> {config['size_multiplier']}x avg) "
                    f"indicates a large participant(s) accumulating or distributing. "
                    f"This creates directional pressure on price."
                ),
                "metrics": {
                    "buy_volume": buy_volume,
                    "sell_volume": sell_volume,
                    "buy_ratio": round(buy_ratio, 2),
                    "sell_ratio": round(sell_ratio, 2),
                    "imbalance": round(max(buy_imbalance, sell_imbalance), 2),
                    "large_order_count": len(spikes),
                    "largest_order_size": largest_spike.get("volume", 0),
                    "avg_trade_size": avg_trade_size,
                },
            }
        )

    return anomalies
