from openai import OpenAI
from app.core.config import settings

_client = OpenAI(api_key=settings.openai_api_key)


def embed(text: str) -> list[float]:
    resp = _client.embeddings.create(
        input=text,
        model=settings.embedding_model,
        dimensions=settings.embedding_dimension,
    )
    return resp.data[0].embedding
