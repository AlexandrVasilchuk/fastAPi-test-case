from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from domain.dto import PredictionStatsDTO
from domain.entities import PredictionLog

# Type variables for generic repository
T = TypeVar("T")
ID = TypeVar("ID")


class BaseRepository(ABC, Generic[T, ID]):
    """Базовый интерфейс репозитория с использованием generics"""

    @abstractmethod
    async def create(self, entity: T) -> T:
        """Создать новую сущность"""
        pass

    @abstractmethod
    async def get_by_id(self, entity_id: ID) -> Optional[T]:
        """Получить сущность по ID"""
        pass

    @abstractmethod
    async def get_all(self) -> List[T]:
        """Получить все сущности"""
        pass

    @abstractmethod
    async def update(self, entity: T) -> T:
        """Обновить сущность"""
        pass

    @abstractmethod
    async def delete(self, entity_id: ID) -> bool:
        """Удалить сущность по ID"""
        pass


class PredictionLogRepository(BaseRepository[PredictionLog, int]):
    """Интерфейс репозитория для работы с логами предсказаний"""

    @abstractmethod
    async def get_stats(
        self, model_name: str, from_date: datetime, to_date: datetime
    ) -> PredictionStatsDTO:
        """Получить статистику по модели за период"""
        pass
