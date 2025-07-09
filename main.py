from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from infrastructure.database import engine
from presentation.controllers import router

import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ждем готовности базы данных
    print("Ожидание готовности базы данных...")
    max_retries = 30
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            from sqlalchemy import text
            async with engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            print(" База данных готова")
            break
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Попытка {attempt + 1}/{max_retries}: База данных еще не готова, ждем {retry_delay}с...")
                await asyncio.sleep(retry_delay)
            else:
                print(f"Не удалось подключиться к базе данных после {max_retries} попыток: {e}")
                exit(1)
    
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
