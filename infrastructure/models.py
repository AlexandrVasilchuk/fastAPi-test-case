from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PredictionLogModel(Base):
    """SQLAlchemy модель для таблицы логов предсказаний"""

    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, nullable=False, index=True)
    duration_ms = Column(Integer, nullable=False)
    was_successful = Column(Boolean, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
