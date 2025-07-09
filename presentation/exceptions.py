from fastapi import HTTPException


class PresentationException(Exception):
    """Базовое исключение слоя представления"""

    pass


class APIException(PresentationException):
    """Исключение для API ошибок"""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(message)


def create_http_exception(status_code: int, message: str) -> HTTPException:
    """Создать HTTP исключение с безопасным сообщением"""
    return HTTPException(status_code=status_code, detail=message)
