"""
Substituição local de embedding_service + pinecone_service.
Usa similaridade de Jaccard (sobreposição de palavras) para recuperação.
Chunks carregados de data/chunks.json (gerado por ingest_html.py).
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


_STOPWORDS = {
    "o", "a", "os", "as", "um", "uma", "uns", "umas",
    "de", "da", "do", "das", "dos", "em", "na", "no", "nas", "nos",
    "para", "por", "com", "que", "se", "é", "e", "ou",
    "ao", "à", "às", "aos", "mais", "mas", "como", "qual", "quais",
    "este", "esta", "estes", "estas", "esse", "essa", "isso", "isto",
    "seu", "sua", "seus", "suas", "me", "te", "nos", "lhe", "lhes",
}


def _tokenize(text: str) -> set[str]:
    import re
    tokens = re.sub(r"[^\w\s]", " ", text.lower()).split()
    return {t for t in tokens if t not in _STOPWORDS and len(t) > 1}


def _score(query: str, doc: str) -> float:
    """Overlap coefficient: |A∩B| / |A|  (fração das palavras da query no doc).
    Melhor que Jaccard para queries curtas contra chunks longos."""
    tq, td = _tokenize(query), _tokenize(doc)
    if not tq:
        return 0.0
    return len(tq & td) / len(tq)


@dataclass
class Match:
    metadata: dict
    score: float


def search(query: str, top_k: int = 5, filter: Optional[dict] = None) -> list[Match]:
    """
    Busca os top_k chunks mais similares à query por Jaccard.
    filter: dict opcional com {"aula": "aula01"} para restringir por aula.
    Interface compatível com pinecone_service.query().
    """
    chunks = _load_chunks()

    if filter and "aula" in filter:
        aula = filter["aula"]
        chunks = [c for c in chunks if c.get("aula") == aula]

    scored = [
        Match(metadata=c, score=_score(query, c["text"]))
        for c in chunks
    ]
    scored.sort(key=lambda m: m.score, reverse=True)
    return scored[:top_k]
