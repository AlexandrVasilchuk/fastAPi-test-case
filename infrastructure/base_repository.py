from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from domain.repositories import BaseRepository

T = TypeVar("T")
ID = TypeVar("ID")
ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class SQLAlchemyBaseRepository(BaseRepository[T, ID], Generic[T, ID, ModelType]):
    """Базовая реализация репозитория с использованием SQLAlchemy"""

    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    async def create(self, entity: T) -> T:
        """Создать новую сущность"""
        db_model = self._entity_to_model(entity)
        self.session.add(db_model)
        await self.session.commit()
        await self.session.refresh(db_model)
        return self._model_to_entity(db_model)

    async def get_by_id(self, entity_id: ID) -> Optional[T]:
        """Получить сущность по ID"""
        query = select(self.model).where(self.model.id == entity_id)
        result = await self.session.execute(query)
        db_model = result.scalar_one_or_none()

        if db_model is None:
            return None

        return self._model_to_entity(db_model)

    async def get_all(self) -> List[T]:
        """Получить все сущности"""
        query = select(self.model)
        result = await self.session.execute(query)
        db_models = result.scalars().all()

        return [self._model_to_entity(model) for model in db_models]

    async def update(self, entity: T) -> T:
        """Обновить сущность"""
        if not hasattr(entity, "id") or entity.id is None:
            raise ValueError("Cannot update entity without ID")

        query = select(self.model).where(self.model.id == entity.id)
        result = await self.session.execute(query)
        db_model = result.scalar_one_or_none()

        if db_model is None:
            raise ValueError(f"Entity with ID {entity.id} not found")

        # Обновляем поля
        self._update_model_from_entity(db_model, entity)

        await self.session.commit()
        await self.session.refresh(db_model)

        return self._model_to_entity(db_model)

    async def delete(self, entity_id: ID) -> bool:
        """Удалить сущность по ID"""
        query = select(self.model).where(self.model.id == entity_id)
        result = await self.session.execute(query)
        db_model = result.scalar_one_or_none()

        if db_model is None:
            return False

        await self.session.delete(db_model)
        await self.session.commit()
        return True

    def _entity_to_model(self, entity: T) -> ModelType:
        """Преобразовать доменную сущность в модель SQLAlchemy"""
        raise NotImplementedError("Subclasses must implement _entity_to_model")

    def _model_to_entity(self, model: ModelType) -> T:
        """Преобразовать модель SQLAlchemy в доменную сущность"""
        raise NotImplementedError("Subclasses must implement _model_to_entity")

    def _update_model_from_entity(self, model: ModelType, entity: T) -> None:
        """Обновить модель SQLAlchemy из доменной сущности"""
        raise NotImplementedError("Subclasses must implement _update_model_from_entity")
