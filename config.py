from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database settings
    database_url: str = (
        "postgresql+asyncpg://postgres:password@localhost:5432/ml_logging_db"
    )
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "ml_logging_db"
    db_user: str = "postgres"
    db_password: str = "password"

    # Application settings
    app_name: str = "ML Prediction Logging Service"
    app_version: str = "1.0.0"
    debug: bool = False

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
