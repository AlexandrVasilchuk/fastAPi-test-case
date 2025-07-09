from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from application.schemas import (
    PredictionLogCreate,
    PredictionLogResponse,
    PredictionStatsResponse,
)
from application.use_cases import GetPredictionStatsUseCase, LogPredictionUseCase
from domain.services import PredictionLogService
from infrastructure.database import get_db_session
from infrastructure.repositories import SQLAlchemyPredictionLogRepository
from utils.logger import log_error

router = APIRouter()


def get_prediction_service(
    session: AsyncSession = Depends(get_db_session),
) -> PredictionLogService:
    """Dependency для получения сервиса предсказаний"""
    repository = SQLAlchemyPredictionLogRepository(session)
    return PredictionLogService(repository)


@router.post("/predict-log", response_model=PredictionLogResponse)
async def log_prediction(
    data: PredictionLogCreate,
    service: PredictionLogService = Depends(get_prediction_service),
):
    """Записать лог предсказания ML-модели"""
    try:
        use_case = LogPredictionUseCase(service)
        result = await use_case.execute(data)
        return result
    except ValueError as e:
        log_error(e, "log_prediction validation")
        raise HTTPException(400, f"Неверные данные запроса {str(e)}")
    except Exception as e:
        log_error(e, "log_prediction")
        raise HTTPException(500, "Внутренняя ошибка сервера")


@router.get("/predictions", response_model=list[PredictionLogResponse])
async def get_all_predictions(
    service: PredictionLogService = Depends(get_prediction_service),
):
    """Получить все логи предсказаний"""
    try:
        predictions = await service.get_all_predictions()
        return [
            PredictionLogResponse(
                id=pred.id,
                model_name=pred.model_name,
                duration_ms=pred.duration_ms,
                was_successful=pred.was_successful,
                timestamp=pred.timestamp,
            )
            for pred in predictions
        ]
    except Exception as e:
        log_error(e, "get_all_predictions")
        raise HTTPException(500, "Внутренняя ошибка сервера")


@router.get("/predictions/{prediction_id}", response_model=PredictionLogResponse)
async def get_prediction_by_id(
    prediction_id: int = Path(..., description="ID предсказания"),
    service: PredictionLogService = Depends(get_prediction_service),
):
    """Получить лог предсказания по ID"""
    try:
        prediction = await service.get_prediction_by_id(prediction_id)
        if prediction is None:
            raise HTTPException(404, "Предсказание не найдено")

        return PredictionLogResponse(
            id=prediction.id,
            model_name=prediction.model_name,
            duration_ms=prediction.duration_ms,
            was_successful=prediction.was_successful,
            timestamp=prediction.timestamp,
        )
    except HTTPException:
        raise
    except Exception as e:
        log_error(e, "get_prediction_by_id")
        raise HTTPException(500, "Внутренняя ошибка сервера")


@router.delete("/predictions/{prediction_id}")
async def delete_prediction(
    prediction_id: int = Path(..., description="ID предсказания"),
    service: PredictionLogService = Depends(get_prediction_service),
):
    """Удалить лог предсказания по ID"""
    try:
        deleted = await service.delete_prediction(prediction_id)
        if not deleted:
            raise HTTPException(404, "Предсказание не найдено")

        return {"message": "Предсказание успешно удалено"}
    except HTTPException:
        raise
    except Exception as e:
        log_error(e, "delete_prediction")
        raise HTTPException(500, "Внутренняя ошибка сервера")


@router.get("/stats", response_model=PredictionStatsResponse)
async def get_stats(
    model_name: str = Query(..., description="Название модели"),
    from_date: str = Query(..., description="Начальная дата (YYYY-MM-DD)"),
    to_date: str = Query(..., description="Конечная дата (YYYY-MM-DD)"),
    service: PredictionLogService = Depends(get_prediction_service),
):
    """Получить статистику предсказаний по модели за период"""
    try:
        # Парсим даты
        from_dt = datetime.fromisoformat(from_date)
        to_dt = datetime.fromisoformat(to_date)
        # Убираем timezone для совместимости с PostgreSQL
        if from_dt.tzinfo is not None:
            from_dt = from_dt.replace(tzinfo=None)
        if to_dt.tzinfo is not None:
            to_dt = to_dt.replace(tzinfo=None)

        use_case = GetPredictionStatsUseCase(service)
        result = await use_case.execute(model_name, from_dt, to_dt)
        return result
    except ValueError as e:
        log_error(e, "get_stats date parsing")
        raise HTTPException(400, "Неверный формат даты")
    except Exception as e:
        log_error(e, "get_stats")
        raise HTTPException(500, "Внутренняя ошибка сервера")
