from app.services.local_study_plan_service import generate_plan as _local_generate_plan
from app.api.schemas.study_plan_schema import StudyPlanRequest, StudyPlanResponse


def generate_plan(req: StudyPlanRequest) -> StudyPlanResponse:
    return _local_generate_plan(req)
