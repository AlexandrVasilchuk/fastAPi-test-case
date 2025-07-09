# ML Prediction Logging Service

Микросервис для логирования обращений к ML-моделям с использованием чистой архитектуры, FastAPI, SQLAlchemy и PostgreSQL.

## Архитектура

Проект построен по принципам чистой архитектуры с разделением на слои:

- **Domain** - доменные сущности, интерфейсы репозиториев, бизнес-логика и DTO
- **Application** - use cases и схемы валидации (Pydantic)
- **Infrastructure** - реализация репозиториев, модели SQLAlchemy, конфигурация БД
- **Presentation** - FastAPI контроллеры и роутеры

## Требования

- Python 3.8+
- PostgreSQL
- Poetry

## Установка и запуск

### 1. Клонирование и установка зависимостей

```bash
git clone <repository-url>
cd test
poetry install
```

### 2. Настройка базы данных PostgreSQL

Создайте базу данных PostgreSQL:

```sql
CREATE DATABASE ml_logging_db;
CREATE USER postgres WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE ml_logging_db TO postgres;
```

### 3. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/ml_logging_db
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ml_logging_db
DB_USER=postgres
DB_PASSWORD=password
DEBUG=false
```

### 4. Применение миграций базы данных

Перед запуском приложения необходимо применить миграции:

```bash
# Применить все миграции
python scripts/migrate.py upgrade head

# Или с помощью alembic напрямую
alembic upgrade head
```

### 5. Запуск приложения

```bash
poetry run python main.py
```

Или с помощью uvicorn:

```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Приложение будет доступно по адресу: http://localhost:8000

## API Endpoints

### Документация API

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Основные эндпоинты

#### POST /api/v1/predict-log

Логирование результата работы ML-модели.

**Пример запроса:**
```json
{
  "model_name": "apartment_price_v1",
  "duration_ms": 124,
  "was_successful": true,
  "timestamp": "2025-06-09T12:00:00"
}
```

**Пример ответа:**
```json
{
  "id": 1,
  "model_name": "apartment_price_v1",
  "duration_ms": 124,
  "was_successful": true,
  "timestamp": "2025-06-09T12:00:00"
}
```

#### GET /api/v1/predictions

Получение всех логов предсказаний.

**Пример ответа:**
```json
[
  {
    "id": 1,
    "model_name": "apartment_price_v1",
    "duration_ms": 124,
    "was_successful": true,
    "timestamp": "2025-06-09T12:00:00"
  }
]
```

#### GET /api/v1/predictions/{prediction_id}

Получение конкретного лога предсказания по ID.

**Пример ответа:**
```json
{
  "id": 1,
  "model_name": "apartment_price_v1",
  "duration_ms": 124,
  "was_successful": true,
  "timestamp": "2025-06-09T12:00:00"
}
```

#### DELETE /api/v1/predictions/{prediction_id}

Удаление лога предсказания по ID.

**Пример ответа:**
```json
{
  "message": "Предсказание успешно удалено"
}
```

#### GET /api/v1/stats

Получение агрегированной статистики по модели за период.

**Параметры запроса:**
- `model_name` (string) - название модели
- `from_date` (string) - начальная дата в формате YYYY-MM-DD
- `to_date` (string) - конечная дата в формате YYYY-MM-DD

**Пример запроса:**
```
GET /api/v1/stats?model_name=apartment_price_v1&from=2025-06-01&to=2025-06-09
```

**Пример ответа:**
```json
{
  "total_requests": 500,
  "successful_requests": 480,
  "average_duration_ms": 132.6
}
```

### Дополнительные эндпоинты

- `GET /` - информация о сервисе
- `GET /health` - проверка здоровья сервиса
- `GET /ready` - проверка готовности сервиса к работе

## Тестирование

### Запуск тестов

```bash
poetry run pytest tests/ -v
```

### Запуск тестов с покрытием

```bash
poetry run pytest tests/ --cov=. --cov-report=html
```

## Структура проекта

```
test/
├── domain/                 # Доменный слой
│   ├── entities.py        # Доменные сущности
│   ├── dto.py            # DTO для передачи данных
│   ├── exceptions.py     # Доменные исключения
│   ├── repositories.py   # Интерфейсы репозиториев (с generics)
│   └── services.py       # Доменные сервисы
├── application/           # Слой приложения
│   ├── schemas.py        # Pydantic схемы
│   ├── use_cases.py      # Use cases
│   └── exceptions.py     # Исключения приложения
├── infrastructure/        # Инфраструктурный слой
│   ├── database.py       # Конфигурация БД
│   ├── models.py         # SQLAlchemy модели
│   ├── base_repository.py # Базовая реализация репозитория
│   └── repositories.py   # Реализация репозиториев
├── presentation/          # Слой представления
│   ├── controllers.py    # FastAPI контроллеры
│   └── exceptions.py     # Исключения представления
├── utils/                 # Утилиты
│   └── logger.py         # Логирование
├── tests/                 # Тесты
│   ├── conftest.py       # Конфигурация pytest
│   └── test_api.py       # Тесты API
├── main.py               # Точка входа приложения
├── config.py             # Конфигурация
├── pyproject.toml        # Poetry конфигурация
└── README.md            # Документация
```

## Особенности реализации

### Чистая архитектура

- Разделение на слои с четкими границами ответственности
- Инверсия зависимостей через интерфейсы
- Независимость доменной логики от внешних зависимостей
- Использование DTO для передачи данных между слоями

### Generic репозитории

- Базовый интерфейс `BaseRepository[T, ID]` с использованием generics
- Абстрактная реализация `SQLAlchemyBaseRepository` для переиспользования кода
- Типобезопасность и единообразие CRUD операций
- Легкое добавление новых сущностей

### Асинхронность

- Полностью асинхронный стек: FastAPI + SQLAlchemy async + asyncpg
- Эффективная работа с базой данных PostgreSQL

### Валидация данных

- Pydantic схемы для валидации входных и выходных данных
- Автоматическая генерация документации API

### Безопасность

- Безопасная обработка ошибок без раскрытия внутренних деталей
- Кастомные исключения для каждого слоя
- Валидация всех входных данных
- Логирование ошибок для отладки

### Тестирование

- Unit-тесты с использованием pytest и httpx.AsyncClient
- Тестовая база данных SQLite в памяти
- Фикстуры для изоляции тестов
- Покрытие всех CRUD операций

## Управление зависимостями

Проект использует Poetry для управления зависимостями:

```bash
# Установка зависимостей
poetry install

# Добавление новой зависимости
poetry add package-name

# Добавление dev зависимости
poetry add --group dev package-name

# Обновление зависимостей
poetry update
```

## Развертывание

### Docker (опционально)

Создайте `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Установка Poetry
RUN pip install poetry

# Копирование конфигурации Poetry
COPY pyproject.toml poetry.lock ./

# Установка зависимостей
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Копирование кода
COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Миграции базы данных

Для управления схемой базы данных используется Alembic:

```bash
# Применение миграций
python scripts/migrate.py upgrade head

# Откат миграций
python scripts/migrate.py downgrade base

# Просмотр текущей версии
python scripts/migrate.py current

# Просмотр истории миграций
python scripts/migrate.py history

# Создание новой миграции (автогенерация)
python scripts/migrate.py revision --autogenerate -m "Описание изменений"

# Или с помощью alembic напрямую
alembic upgrade head
alembic downgrade base
alembic current
alembic history
alembic revision --autogenerate -m "Описание изменений"
```

## Мониторинг и логирование

- Встроенные эндпоинты для проверки здоровья сервиса (`/health`, `/ready`)
- Логирование SQL запросов (в режиме разработки)
- CORS middleware для веб-интерфейса
- Безопасная обработка ошибок с логированием

## Безопасность

- Валидация всех входных данных
- Безопасная обработка ошибок без раскрытия внутренних деталей
- Защита от SQL-инъекций через SQLAlchemy ORM
- Кастомные исключения для каждого слоя архитектуры
- Логирование ошибок для отладки без раскрытия информации пользователю

## Расширение функциональности

### Добавление новой сущности

1. Создайте доменную сущность в `domain/entities.py`
2. Создайте интерфейс репозитория, наследуясь от `BaseRepository`
3. Создайте SQLAlchemy модель в `infrastructure/models.py`
4. Реализуйте репозиторий, наследуясь от `SQLAlchemyBaseRepository`
5. Добавьте методы в доменный сервис
6. Создайте use cases и схемы
7. Добавьте контроллеры

### Пример добавления новой сущности

```python
# domain/entities.py
@dataclass
class User:
    id: Optional[int] = None
    name: str
    email: str

# domain/repositories.py
class UserRepository(BaseRepository[User, int]):
    pass

# infrastructure/models.py
class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

# infrastructure/repositories.py
class SQLAlchemyUserRepository(SQLAlchemyBaseRepository[User, int, UserModel], UserRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserModel)
    
    def _entity_to_model(self, entity: User) -> UserModel:
        return UserModel(name=entity.name, email=entity.email)
    
    def _model_to_entity(self, model: UserModel) -> User:
        return User(id=model.id, name=model.name, email=model.email)
    
    def _update_model_from_entity(self, model: UserModel, entity: User) -> None:
        model.name = entity.name
        model.email = entity.email
```

