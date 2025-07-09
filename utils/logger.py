import logging
from typing import Optional

from config import settings

# Настройка логирования
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def log_error(error: Exception, context: Optional[str] = None) -> None:
    """Логирует ошибку для отладки без раскрытия деталей пользователю"""
    error_message = f"Error in {context or 'unknown context'}: {str(error)}"
    logger.error(error_message, exc_info=True)


def log_info(message: str) -> None:
    """Логирует информационное сообщение"""
    logger.info(message)


def log_debug(message: str) -> None:
    """Логирует отладочное сообщение"""
    if settings.debug:
        logger.debug(message)
