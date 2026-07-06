"""
Planejador de estudos determinístico — sem LLM.
Mapeia fraquezas identificadas no quiz para passos de estudo pré-definidos.
"""
from app.api.schemas.study_plan_schema import StudyPlanRequest, StudyPlanResponse, StudyStep

# Mapa: substring da fraqueza (lower) → StudyStep base
_WEAKNESS_MAP: list[tuple[str, StudyStep]] = [
    ("definição de ia", StudyStep(
        order=1, topic="Definição de Inteligência Artificial",
        description="Revisar as principais definições de IA: sistemas que pensam/agem humanamente vs. racionalmente.",
        source="Aula 01 — Panorama da IA",
    )),
    ("teste de turing", StudyStep(
        order=1, topic="Teste de Turing",
        description="Entender o propósito do teste, suas limitações e por que é marco histórico da IA.",
        source="Aula 01 — Panorama da IA",
    )),
    ("ia fraca", StudyStep(
        order=1, topic="IA Fraca vs IA Geral",
        description="Diferenciar narrow AI (sistemas especializados) de AGI (inteligência geral).",
        source="Aula 01 — Panorama da IA",
    )),
    ("racionalidade", StudyStep(
        order=2, topic="Racionalidade de Agentes",
        description="Revisar a definição de agente racional: maximizar desempenho com base em percepção e conhecimento.",
        source="Aula 02 — Agentes Inteligentes",
    )),
    ("percepção", StudyStep(
        order=2, topic="Ciclo Percepção-Decisão-Ação",
        description="Estudar o ciclo básico do agente: perceber o ambiente, decidir e agir.",
        source="Aula 02 — Agentes Inteligentes",
    )),
    ("ambiente", StudyStep(
        order=2, topic="Tipos de Ambiente",
        description="Revisar as propriedades dos ambientes: observável, determinístico, episódico, estático, discreto.",
        source="Aula 02 — Agentes Inteligentes",
    )),
    ("bfs", StudyStep(
        order=3, topic="Busca em Largura (BFS)",
        description="Revisar a estrutura FIFO do BFS, completude e otimalidade quando custos são iguais.",
        source="Aula 03 — Busca e Otimização",
    )),
    ("heurística", StudyStep(
        order=3, topic="Heurísticas e Algoritmo A*",
        description="Estudar heurísticas admissíveis e a função f(n) = g(n) + h(n) do A*.",
        source="Aula 03 — Busca e Otimização",
    )),
    ("hill climbing", StudyStep(
        order=4, topic="Hill Climbing e Limitações",
        description="Revisar por que Hill Climbing fica preso em ótimos locais, platôs e cristas.",
        source="Aula 04 — Busca Local e Adversarial",
    )),
    ("minimax", StudyStep(
        order=4, topic="Minimax e Poda Alfa-Beta",
        description="Estudar a estratégia MIN no Minimax e como a poda alfa-beta elimina ramos irrelevantes.",
        source="Aula 04 — Busca Local e Adversarial",
    )),
    ("poda alfa", StudyStep(
        order=4, topic="Poda Alfa-Beta",
        description="Entender como a poda elimina ramos sem afetar o resultado do Minimax.",
        source="Aula 04 — Busca Local e Adversarial",
    )),
    ("rag", StudyStep(
        order=5, topic="RAG — Retrieval-Augmented Generation",
        description="Revisar como RAG combina recuperação de informação com geração por LLM para reduzir alucinações.",
        source="Aula 05 — Representação do Conhecimento",
    )),
    ("embedding", StudyStep(
        order=5, topic="Embeddings e Representação Vetorial",
        description="Estudar como textos são convertidos em vetores numéricos e usados em busca semântica.",
        source="Aula 05 — Representação do Conhecimento",
    )),
    ("lógica proposicional", StudyStep(
        order=5, topic="Lógica Proposicional",
        description="Revisar tabelas-verdade e a semântica de P → Q (falso só quando P=V e Q=F).",
        source="Aula 05 — Representação do Conhecimento",
    )),
    ("overfitting", StudyStep(
        order=6, topic="Overfitting e Underfitting",
        description="Entender quando um modelo performa bem no treino mas mal em dados novos e como mitigar.",
        source="Aula 06 — ML Supervisionado",
    )),
    ("métricas", StudyStep(
        order=6, topic="Métricas de Classificação",
        description="Revisar Acurácia, Precisão, Recall e F1-Score — quando usar cada uma.",
        source="Aula 06 — ML Supervisionado",
    )),
    ("regressão", StudyStep(
        order=6, topic="Regressão Linear",
        description="Estudar o modelo y = ax + b e sua interpretação geométrica.",
        source="Aula 06 — ML Supervisionado",
    )),
    ("k-means", StudyStep(
        order=7, topic="Clustering K-Means",
        description="Revisar o algoritmo de clustering não supervisionado e como os centroides são atualizados.",
        source="Aula 07 — Clustering e Ensembles",
    )),
    ("random forest", StudyStep(
        order=7, topic="Random Forest",
        description="Entender como múltiplas árvores de decisão independentes formam um ensemble.",
        source="Aula 07 — Clustering e Ensembles",
    )),
    ("bagging", StudyStep(
        order=7, topic="Técnica de Bagging",
        description="Revisar como Bagging reduz variância combinando modelos treinados em subamostras.",
        source="Aula 07 — Clustering e Ensembles",
    )),
]

_REVISAO_GERAL = [
    StudyStep(order=1, topic="Panorama da IA", description="Revisar definições, histórico e aplicações da IA.", source="Aula 01 — Panorama da IA"),
    StudyStep(order=2, topic="Agentes Inteligentes", description="Estudar o ciclo percepção-decisão-ação e tipos de ambiente.", source="Aula 02 — Agentes Inteligentes"),
    StudyStep(order=3, topic="Busca e Otimização", description="Revisar BFS, DFS, A* e heurísticas admissíveis.", source="Aula 03 — Busca e Otimização"),
    StudyStep(order=5, topic="Representação do Conhecimento", description="Aprofundar RAG, embeddings e lógica proposicional.", source="Aula 05 — Representação do Conhecimento"),
]


def _match(weakness: str, keyword: str) -> bool:
    return keyword in weakness.lower()


def generate_plan(req: StudyPlanRequest) -> StudyPlanResponse:
    if not req.weaknesses:
        return StudyPlanResponse(title="Plano de Revisão Geral", steps=_REVISAO_GERAL)

    steps: list[StudyStep] = []
    seen: set[str] = set()

    for weakness in req.weaknesses:
        for keyword, step in _WEAKNESS_MAP:
            if _match(weakness, keyword) and step.topic not in seen:
                steps.append(step)
                seen.add(step.topic)
                break

    # Fallback: fraqueza não mapeada → revisão geral da aula mais próxima
    if not steps:
        steps = _REVISAO_GERAL

    steps.sort(key=lambda s: s.order)
    # Renumerar order sequencialmente
    for i, s in enumerate(steps, 1):
        s.order = i

    return StudyPlanResponse(title="Plano de Estudo Personalizado", steps=steps)
