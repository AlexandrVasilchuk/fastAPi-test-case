from datetime import datetime

from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.dto import PredictionStatsDTO
from domain.entities import PredictionLog
from domain.repositories import PredictionLogRepository
from infrastructure.base_repository import SQLAlchemyBaseRepository
from infrastructure.models import PredictionLogModel


class SQLAlchemyPredictionLogRepository(
    SQLAlchemyBaseRepository[PredictionLog, int, PredictionLogModel],
    PredictionLogRepository,
):
    """Реализация репозитория с использованием SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, PredictionLogModel)

    def _entity_to_model(self, entity: PredictionLog) -> PredictionLogModel:
        """Преобразовать доменную сущность в модель SQLAlchemy"""
        return PredictionLogModel(
            model_name=entity.model_name,
            duration_ms=entity.duration_ms,
            was_successful=entity.was_successful,
            timestamp=entity.timestamp,
        )

    def _model_to_entity(self, model: PredictionLogModel) -> PredictionLog:
        """Преобразовать модель SQLAlchemy в доменную сущность"""
        return PredictionLog(
            id=model.id,
            model_name=model.model_name,
            duration_ms=model.duration_ms,
            was_successful=model.was_successful,
            timestamp=model.timestamp,
        )

    def _update_model_from_entity(
        self, model: PredictionLogModel, entity: PredictionLog
    ) -> None:
        """Обновить модель SQLAlchemy из доменной сущности"""
        model.model_name = entity.model_name
        model.duration_ms = entity.duration_ms
        model.was_successful = entity.was_successful
        model.timestamp = entity.timestamp

    async def get_stats(
        self, model_name: str, from_date: datetime, to_date: datetime
    ) -> PredictionStatsDTO:
        """Получить статистику по модели за период"""
        # Запрос для получения общей статистики
        query = select(
            func.count().label("total_requests"),
            func.sum(case((PredictionLogModel.was_successful, 1), else_=0)).label(
                "successful_requests"
            ),
            func.avg(PredictionLogModel.duration_ms).label("average_duration_ms"),
        ).where(
            PredictionLogModel.model_name == model_name,
            PredictionLogModel.timestamp >= from_date,
            PredictionLogModel.timestamp <= to_date,
        )

        result = await self.session.execute(query)
        row = result.first()

        return PredictionStatsDTO(
            total_requests=row.total_requests or 0,
            successful_requests=row.successful_requests or 0,
            average_duration_ms=float(row.average_duration_ms or 0.0),
        )
