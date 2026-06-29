from fastapi import APIRouter
from app.api.schemas.rag_schema import RagMatch, RagMatchMetadata, RagSearchRequest, RagSearchResponse
from app.services.embedding_service import embed
from app.services.pinecone_service import query

router = APIRouter(prefix="/rag", tags=["rag"])


@router.post("/search", response_model=RagSearchResponse)
def rag_search(req: RagSearchRequest) -> RagSearchResponse:
    vector = embed(req.query)
    filter_ = {"aula": req.topic_id} if req.topic_id else None
    matches = query(vector, top_k=req.top_k, filter=filter_)

    results = [
        RagMatch(
            text=m.metadata.get("text", ""),
            score=round(m.score, 4),
            metadata=RagMatchMetadata(
                aula=m.metadata.get("aula"),
                titulo_aula=m.metadata.get("titulo_aula"),
                pagina=m.metadata.get("pagina"),
                topico=m.metadata.get("topico"),
            ),
        )
        for m in matches
    ]
    return RagSearchResponse(matches=results)
