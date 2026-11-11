from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "URL Shortener API"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = ""
    DATABASE_URL: str = "sqlite:///./shortener.db"
    BASE_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
