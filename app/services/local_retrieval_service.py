"""
Substituição local de embedding_service + pinecone_service.
Usa similaridade de Jaccard (sobreposição de palavras) para recuperação.
Chunks carregados de data/chunks.json (gerado por ingest_local.py).
"""
import json
import os
from dataclasses import dataclass
from typing import Optional

_CHUNKS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "chunks.json")
_chunks: list[dict] | None = None


def _load_chunks() -> list[dict]:
    global _chunks
    if _chunks is None:
        path = os.path.abspath(_CHUNKS_PATH)
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Arquivo de chunks não encontrado: {path}\n"
                "Execute `python ingest_local.py` primeiro."
            )
        with open(path, encoding="utf-8") as f:
            _chunks = json.load(f)
    return _chunks


def _tokenize(text: str) -> set[str]:
    return set(text.lower().replace(".", "").replace(",", "").replace("?", "").split())


def _jaccard(a: str, b: str) -> float:
    ta, tb = _tokenize(a), _tokenize(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


@dataclass
class Match:
    metadata: dict
    score: float


def search(query: str, top_k: int = 5, filter: Optional[dict] = None) -> list[Match]:
    """
    Busca os top_k chunks mais similares à query por Jaccard.
    Parâmetro `filter` ignorado (não há metadados de aula nos chunks locais).
    Interface compatível com pinecone_service.query().
    """
    chunks = _load_chunks()
    scored = [
        Match(metadata=c, score=_jaccard(query, c["text"]))
        for c in chunks
    ]
    scored.sort(key=lambda m: m.score, reverse=True)
    return scored[:top_k]
