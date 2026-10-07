from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://fixit:fixit@localhost:5432/fixit"
    jwt_secret: str = "change-me"
    jwt_expire_minutes: int = 1440
    frontend_url: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
