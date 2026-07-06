from pinecone import Pinecone
from app.core.config import settings

_pc = Pinecone(api_key=settings.pinecone_api_key)
_index = _pc.Index(host=settings.pinecone_host)


def query(vector: list[float], top_k: int = 5, filter: dict | None = None) -> list:
    kwargs: dict = dict(
        vector=vector,
        top_k=top_k,
        namespace=settings.pinecone_namespace,
        include_metadata=True,
    )
    if filter:
        kwargs["filter"] = filter
    result = _index.query(**kwargs)
    return result.matches
