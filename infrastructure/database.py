from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from config import settings


# Создаем асинхронный движок для PostgreSQL
# Используем ленивый импорт для избежания ошибок в тестах
def get_engine():
    try:
        from sqlalchemy.ext.asyncio import create_async_engine

        return create_async_engine(
            settings.database_url,
            echo=True,  # Логирование SQL запросов
            future=True,
        )
    except ImportError:
        # Для тестов используем SQLite
        from sqlalchemy.ext.asyncio import create_async_engine

        return create_async_engine(
            "sqlite+aiosqlite:///:memory:", echo=True, future=True
        )


engine = get_engine()

# Создаем фабрику асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db_session() -> AsyncSession:
    """Получить асинхронную сессию базы данных"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
