from pydantic import BaseModel


class StudyPlanRequest(BaseModel):
    weaknesses: list[str]
    goal: str = "Revisar para a prova"


class StudyStep(BaseModel):
    order: int
    topic: str
    description: str
    source: str


class StudyPlanResponse(BaseModel):
    title: str
    steps: list[StudyStep]
