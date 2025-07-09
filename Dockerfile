FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Установка Poetry
RUN pip install poetry

# Копирование файлов конфигурации Poetry
COPY pyproject.toml poetry.lock ./

# Настройка Poetry для установки в системный Python
RUN poetry config virtualenvs.create false

# Установка зависимостей (без установки текущего проекта)
RUN poetry install --only main --no-root

# Копирование исходного кода
COPY . .

# Создание пользователя для безопасности
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Открытие порта
EXPOSE 8000

# Команда по умолчанию
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]