from fastapi import APIRouter
from app.api.schemas.chat_schema import ChatRequest, ChatResponse
from app.services import rag_service

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    return rag_service.chat(req)
