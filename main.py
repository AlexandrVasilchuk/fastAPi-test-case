from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from infrastructure.database import engine
from presentation.controllers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Проверяем подключение к базе данных
    try:
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        print("Убедитесь, что миграции применены: alembic upgrade head")
    yield


app = FastAPI(
    title=settings.app_name,
    description="Микросервис для логирования обращений к ML-моделям",
    version=settings.app_version,
    lifespan=lifespan,
    debug=settings.debug,
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(router, prefix="/api/v1", tags=["predictions"])


@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "healthy"}


@app.get("/ready")
async def readiness_check():
    """Проверка готовности сервиса к работе"""
    try:
        # Здесь можно добавить проверки подключения к БД и других зависимостей
        return {"status": "ready"}
    except Exception:
        return {"status": "not ready"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.host, port=settings.port, log_level="info")
