from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "TutorIA CC0121 Backend"
    api_prefix: str = "/api/v1"

    cors_origins: str = "http://localhost:3000,http://localhost:5173,http://localhost:8080"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
