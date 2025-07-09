class DomainException(Exception):
    """Базовое исключение доменного слоя"""

    pass


class PredictionLogException(DomainException):
    """Исключение для ошибок логирования предсказаний"""

    pass


class StatsCalculationException(DomainException):
    """Исключение для ошибок расчета статистики"""

    pass
