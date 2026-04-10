from typing import Any, Optional

from app.detectors.spoofing import detect_spoofing
from app.detectors.absorption import detect_absorption
from app.detectors.aggressive_flow import detect_aggressive_flow


DETECTOR_REGISTRY = {
    "spoofing": detect_spoofing,
    "absorption": detect_absorption,
    "aggressive_flow": detect_aggressive_flow,
}


def detect_anomaly(
    orderbook: dict,
    trades: list,
    metadata: Optional[dict] = None,
    detectors: Optional[list] = None,
) -> dict:
    try:
        if metadata is None:
            metadata = {}

        if not orderbook and not trades:
            return {
                "status": "error",
                "data": None,
                "error": "Missing orderbook and trades data",
            }

        if detectors is None:
            detectors = list(DETECTOR_REGISTRY.keys())

        all_anomalies = []

        for detector_name in detectors:
            if detector_name not in DETECTOR_REGISTRY:
                continue

            detector_func = DETECTOR_REGISTRY[detector_name]
            anomalies = detector_func(orderbook, trades, metadata)
            all_anomalies.extend(anomalies)

        all_anomalies.sort(key=lambda x: x.get("confidence", 0), reverse=True)

        return {
            "status": "success",
            "data": all_anomalies,
            "summary": {
                "total_anomalies": len(all_anomalies),
                "spoofing_count": sum(
                    1 for a in all_anomalies if a["type"] == "spoofing"
                ),
                "absorption_count": sum(
                    1 for a in all_anomalies if a["type"] == "absorption"
                ),
                "aggressive_flow_count": sum(
                    1 for a in all_anomalies if a["type"] == "aggressive_flow"
                ),
            }
            if all_anomalies
            else {"total_anomalies": 0},
            "error": None,
        }

    except Exception as e:
        return {"status": "error", "data": None, "error": str(e)}
