from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "dev"
    data_dir: str = "data"
    raw_dir: str = "data/raw"
    processed_dir: str = "data/processed"
    models_dir: str = "models"

    class Config:
        env_file = ".env"

settings = Settings()
