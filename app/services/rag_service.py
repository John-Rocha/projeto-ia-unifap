from app.services.local_retrieval_service import search
from app.services.local_llm_service import generate
from app.utils.prompt_builder import build_prompt
from app.api.schemas.chat_schema import ChatRequest, ChatResponse, Source

_NO_CONTEXT_ANSWER = (
    "Não encontrei informação suficiente no material da disciplina para responder "
    "com segurança. Tente reformular a pergunta ou pergunte sobre outro tópico."
)


def chat(req: ChatRequest) -> ChatResponse:
    matches = search(req.question, top_k=req.top_k)

    if not matches or matches[0].score == 0.0:
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
