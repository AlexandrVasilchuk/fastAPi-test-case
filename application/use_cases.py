from datetime import datetime

from application.schemas import (
    PredictionLogCreate,
    PredictionLogResponse,
    PredictionStatsResponse,
)
from domain.services import PredictionLogService


class LogPredictionUseCase:
    """Use case для логирования предсказания"""

    def __init__(self, service: PredictionLogService):
        self.service = service

    async def execute(self, data: PredictionLogCreate) -> PredictionLogResponse:
        """Выполнить логирование предсказания"""
        # Используем текущее время если timestamp не указан
        timestamp = data.timestamp or datetime.now(datetime.UTC)
        # Убираем timezone для совместимости с PostgreSQL
        if timestamp.tzinfo is not None:
            timestamp = timestamp.replace(tzinfo=None)

        prediction_log = await self.service.log_prediction(
            model_name=data.model_name,
            duration_ms=data.duration_ms,
            was_successful=data.was_successful,
            timestamp=timestamp,
        )

        return PredictionLogResponse(
            id=prediction_log.id,
            model_name=prediction_log.model_name,
            duration_ms=prediction_log.duration_ms,
            was_successful=prediction_log.was_successful,
            timestamp=prediction_log.timestamp,
        )


class GetPredictionStatsUseCase:
    """Use case для получения статистики предсказаний"""

    def __init__(self, service: PredictionLogService):
        self.service = service

    async def execute(
        self, model_name: str, from_date: datetime, to_date: datetime
    ) -> PredictionStatsResponse:
        """Получить статистику предсказаний"""
        stats = await self.service.get_prediction_stats(
            model_name=model_name, from_date=from_date, to_date=to_date
        )

        return PredictionStatsResponse(
            total_requests=stats.total_requests,
            successful_requests=stats.successful_requests,
            average_duration_ms=stats.average_duration_ms,
        )
