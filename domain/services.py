from datetime import datetime

from domain.dto import PredictionStatsDTO
from domain.entities import PredictionLog
from domain.repositories import PredictionLogRepository


class PredictionLogService:
    """Доменный сервис для работы с логами предсказаний"""

    def __init__(self, repository: PredictionLogRepository):
        self.repository = repository

    async def log_prediction(
        self,
        model_name: str,
        duration_ms: int,
        was_successful: bool,
        timestamp: datetime,
    ) -> PredictionLog:
        """Записать лог предсказания"""
        prediction_log = PredictionLog(
            model_name=model_name,
            duration_ms=duration_ms,
            was_successful=was_successful,
            timestamp=timestamp,
        )

        return await self.repository.create(prediction_log)

    async def get_prediction_by_id(self, prediction_id: int) -> PredictionLog | None:
        """Получить лог предсказания по ID"""
        return await self.repository.get_by_id(prediction_id)

    async def get_all_predictions(self) -> list[PredictionLog]:
        """Получить все логи предсказаний"""
        return await self.repository.get_all()

    async def update_prediction(self, prediction_log: PredictionLog) -> PredictionLog:
        """Обновить лог предсказания"""
        return await self.repository.update(prediction_log)

    async def delete_prediction(self, prediction_id: int) -> bool:
        """Удалить лог предсказания"""
        return await self.repository.delete(prediction_id)

    async def get_prediction_stats(
        self, model_name: str, from_date: datetime, to_date: datetime
    ) -> PredictionStatsDTO:
        """Получить статистику предсказаний"""
        return await self.repository.get_stats(model_name, from_date, to_date)
