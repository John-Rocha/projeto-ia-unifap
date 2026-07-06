from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "TutorIA CC0121 Backend"
    api_prefix: str = "/api/v1"

    pinecone_api_key: str
    pinecone_host: str
    pinecone_namespace: str = "disciplina-ia"

    openai_api_key: str
    embedding_model: str = "text-embedding-3-small"
    embedding_dimension: int = 512

    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.2

    cors_origins: str = "http://localhost:3000,http://localhost:5173,http://localhost:8080"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
