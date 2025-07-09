from dataclasses import dataclass


@dataclass
class PredictionStatsDTO:
    """DTO для статистики предсказаний"""

    total_requests: int
    successful_requests: int
    average_duration_ms: float
