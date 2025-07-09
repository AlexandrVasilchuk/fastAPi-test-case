import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_log_prediction_success(client: AsyncClient):
    """Тест POST /predict-log - успешное логирование предсказания"""
    data = {
        "model_name": "apartment_price_v1",
        "duration_ms": 124,
        "was_successful": True,
        "timestamp": "2025-06-09T12:00:00",
    }

    response = await client.post("/api/v1/predict-log", json=data)

    assert response.status_code == 200
    result = response.json()

    assert result["model_name"] == data["model_name"]
    assert result["duration_ms"] == data["duration_ms"]
    assert result["was_successful"] == data["was_successful"]
    assert "id" in result


@pytest.mark.asyncio
async def test_get_stats_success(client: AsyncClient):
    """Тест GET /stats - получение статистики"""
    # Сначала создаем лог
    log_data = {
        "model_name": "apartment_price_v1",
        "duration_ms": 100,
        "was_successful": True,
        "timestamp": "2025-06-05T12:00:00",
    }
    create_response = await client.post("/api/v1/predict-log", json=log_data)
    print(f"Create response: {create_response.status_code} - {create_response.text}")

    # Получаем статистику
    params = {
        "model_name": "apartment_price_v1",
        "from_date": "2025-06-01",
        "to_date": "2025-06-09",
    }

    response = await client.get("/api/v1/stats", params=params)
    print(f"Stats response: {response.status_code} - {response.text}")

    assert response.status_code == 200
    result = response.json()

    assert "total_requests" in result
    assert "successful_requests" in result
    assert "average_duration_ms" in result
    assert result["total_requests"] >= 1


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Тест GET /health - проверка здоровья сервиса"""
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
