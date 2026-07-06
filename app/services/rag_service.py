from app.services.embedding_service import embed
from app.services.pinecone_service import query
from app.services.llm_service import generate
from app.utils.prompt_builder import build_prompt
from app.api.schemas.chat_schema import ChatRequest, ChatResponse, Source

_NO_CONTEXT_ANSWER = (
    "Não encontrei informação suficiente no material da disciplina para responder "
    "com segurança. Tente reformular a pergunta ou pergunte sobre outro tópico."
)


def chat(req: ChatRequest) -> ChatResponse:
    vector = embed(req.question)

    pinecone_filter = {"aula": req.topic_id} if req.topic_id else None
    matches = query(vector, top_k=req.top_k, filter=pinecone_filter)

    if not matches:
        return ChatResponse(
            answer=_NO_CONTEXT_ANSWER,
            sources=[],
            retrieved_chunks=[],
            confidence=0.0,
        )

    chunks = [m.metadata.get("text", "") for m in matches]
    context = "\n\n".join(chunks)
    prompt = build_prompt(context=context, question=req.question)
    answer = generate(prompt)

    sources = [
        Source(
            aula=m.metadata.get("aula"),
            titulo_aula=m.metadata.get("titulo_aula"),
            tema=m.metadata.get("tema"),
            topico=m.metadata.get("topico"),
            pagina=m.metadata.get("pagina"),
            score=round(m.score, 4),
        )
        for m in matches
    ]
    confidence = round(sum(m.score for m in matches) / len(matches), 4)

    return ChatResponse(
        answer=answer,
        sources=sources,
        retrieved_chunks=chunks,
        confidence=confidence,
    )
