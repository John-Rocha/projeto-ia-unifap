from fastapi import APIRouter
from app.api.schemas.diagnostic_schema import (
    DiagnosticQuizResponse,
    DiagnosticResult,
    DiagnosticSubmitRequest,
)
from app.services import diagnostic_service

router = APIRouter(prefix="/diagnostic", tags=["diagnostic"])


@router.get("/quiz", response_model=DiagnosticQuizResponse)
def get_quiz(topic_id: str) -> DiagnosticQuizResponse:
    return diagnostic_service.get_quiz(topic_id)


@router.post("/submit", response_model=DiagnosticResult)
def submit(req: DiagnosticSubmitRequest) -> DiagnosticResult:
    return diagnostic_service.submit(req)
