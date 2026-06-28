from pydantic import BaseModel


class Source(BaseModel):
    aula: str | None = None
    titulo_aula: str | None = None
    tema: str | None = None
    topico: str | None = None
    pagina: int | None = None
    score: float | None = None


class ChatRequest(BaseModel):
    question: str
    topic_id: str | None = None
    top_k: int = 5


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
    retrieved_chunks: list[str]
    confidence: float | None = None
