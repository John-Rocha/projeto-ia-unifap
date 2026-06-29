from pydantic import BaseModel


class RagSearchRequest(BaseModel):
    query: str
    topic_id: str | None = None
    top_k: int = 5


class RagMatchMetadata(BaseModel):
    aula: str | None = None
    titulo_aula: str | None = None
    pagina: int | None = None
    topico: str | None = None


class RagMatch(BaseModel):
    text: str
    score: float
    metadata: RagMatchMetadata


class RagSearchResponse(BaseModel):
    matches: list[RagMatch]
