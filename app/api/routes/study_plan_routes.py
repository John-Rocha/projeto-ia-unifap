from fastapi import APIRouter
from app.api.schemas.study_plan_schema import StudyPlanRequest, StudyPlanResponse
from app.services import study_plan_service

router = APIRouter(tags=["study-plan"])


@router.post("/study-plan", response_model=StudyPlanResponse)
def create_study_plan(req: StudyPlanRequest) -> StudyPlanResponse:
    return study_plan_service.generate_plan(req)
