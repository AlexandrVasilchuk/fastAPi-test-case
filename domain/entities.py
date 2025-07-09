from dataclasses import dataclass
from datetime import datetime


@dataclass
class PredictionLog:
    """Доменная сущность для логирования предсказаний ML-модели"""

    model_name: str
    duration_ms: int
    was_successful: bool
    timestamp: datetime
    id: int | None = None
