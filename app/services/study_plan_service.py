import json
from app.services.llm_service import generate
from app.api.schemas.study_plan_schema import StudyPlanRequest, StudyPlanResponse, StudyStep

_PROMPT = """Você é um assistente educacional da disciplina de Inteligência Artificial (CC0121).

Crie um plano de estudo personalizado com base nas dificuldades do aluno.

Dificuldades identificadas: {weaknesses}
Objetivo do aluno: {goal}

Retorne APENAS um JSON válido, sem texto adicional, no seguinte formato:
{{
  "title": "Plano de Estudo Personalizado",
  "steps": [
    {{
      "order": 1,
      "topic": "Nome do tópico",
      "description": "O que o aluno deve focar ao estudar este tópico.",
      "source": "Aula XX — Título da Aula"
    }}
  ]
}}

Use apenas conteúdos das aulas da disciplina:
Aula 01 — Panorama da IA
Aula 02 — Agentes Inteligentes
Aula 03 — Busca e Otimização
Aula 04 — Busca Local e Adversarial
Aula 05 — Representação do Conhecimento
Aula 06 — ML Supervisionado
Aula 07 — Clustering e Ensembles

Ordene os tópicos do mais fundamental ao mais avançado."""


def generate_plan(req: StudyPlanRequest) -> StudyPlanResponse:
    weaknesses_str = ", ".join(req.weaknesses) if req.weaknesses else "Revisão geral da disciplina"
    prompt = _PROMPT.format(weaknesses=weaknesses_str, goal=req.goal)
    raw = generate(prompt).strip()

    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    data = json.loads(raw)
    steps = [StudyStep(**s) for s in data.get("steps", [])]
    return StudyPlanResponse(title=data.get("title", "Plano de Estudo Personalizado"), steps=steps)
