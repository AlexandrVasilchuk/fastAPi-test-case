from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PredictionLogCreate(BaseModel):
    """Схема для создания лога предсказания"""

    model_name: str = Field(..., description="Название модели")
    duration_ms: int = Field(..., ge=0, description="Время выполнения в миллисекундах")
    was_successful: bool = Field(..., description="Успешность предсказания")
    timestamp: Optional[datetime] = Field(None, description="Временная метка")


class PredictionLogResponse(BaseModel):
    """Схема ответа для лога предсказания"""

    id: int
    model_name: str
    duration_ms: int
    was_successful: bool
    timestamp: datetime

    class Config:
        from_attributes = True


class PredictionStatsResponse(BaseModel):
    """Схема ответа для статистики предсказаний"""

    total_requests: int
    successful_requests: int
    average_duration_ms: float

    class Config:
        from_attributes = True


class StatsQueryParams(BaseModel):
    """Схема для параметров запроса статистики"""

    model_name: str = Field(..., description="Название модели")
    from_date: datetime = Field(..., description="Начальная дата")
    to_date: datetime = Field(..., description="Конечная дата")
