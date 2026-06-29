from pydantic import BaseModel


class DiagnosticQuestion(BaseModel):
    id: str
    question: str
    options: list[str]


class DiagnosticQuizResponse(BaseModel):
    topic_id: str
    title: str
    questions: list[DiagnosticQuestion]


class AnswerItem(BaseModel):
    question_id: str
    selected_option: str


class DiagnosticSubmitRequest(BaseModel):
    topic_id: str
    answers: list[AnswerItem]


class DiagnosticResult(BaseModel):
    score: int
    total: int
    weaknesses: list[str]
    recommendation: str
