from fastapi import APIRouter

router = APIRouter(tags=["topics"])

_TOPICS = [
    {"id": "aula01", "title": "Panorama da IA", "description": "História, definições e aplicações da IA"},
    {"id": "aula02", "title": "Agentes Inteligentes", "description": "Agentes, ambientes e racionalidade"},
    {"id": "aula03", "title": "Busca e Otimização", "description": "BFS, DFS, A* e heurísticas"},
    {"id": "aula04", "title": "Busca Local e Adversarial", "description": "Hill climbing, Minimax e poda alfa-beta"},
    {"id": "aula05", "title": "Representação do Conhecimento", "description": "Lógica, sistemas especialistas e RAG"},
    {"id": "aula06", "title": "ML Supervisionado", "description": "Regressão, classificação e avaliação de modelos"},
    {"id": "aula07", "title": "Clustering e Ensembles", "description": "K-means, árvores de decisão e Random Forest"},
]


@router.get("/topics")
def list_topics() -> dict:
    return {"topics": _TOPICS}
