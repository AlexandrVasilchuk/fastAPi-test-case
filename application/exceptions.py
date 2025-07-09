class ApplicationException(Exception):
    """Базовое исключение слоя приложения"""

    pass


class ValidationException(ApplicationException):
    """Исключение для ошибок валидации"""

    pass


class UseCaseException(ApplicationException):
    """Исключение для ошибок use cases"""

    pass
