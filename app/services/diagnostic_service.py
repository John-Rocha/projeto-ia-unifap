from app.api.schemas.diagnostic_schema import (
    AnswerItem,
    DiagnosticQuestion,
    DiagnosticQuizResponse,
    DiagnosticResult,
    DiagnosticSubmitRequest,
)
from app.core.exceptions import TopicNotFoundError

_QUIZZES: dict[str, dict] = {
    "aula01": {
        "title": "Diagnóstico — Panorama da IA",
        "questions": [
            DiagnosticQuestion(
                id="a01q1",
                question="Qual definição descreve melhor a Inteligência Artificial?",
                options=[
                    "Programas que seguem regras fixas sem aprender",
                    "Sistemas que simulam capacidades cognitivas humanas",
                    "Hardware especializado para cálculos numéricos",
                    "Banco de dados com muitas informações",
                ],
            ),
            DiagnosticQuestion(
                id="a01q2",
                question="O teste de Turing avalia:",
                options=[
                    "A velocidade de processamento de um computador",
                    "A capacidade de uma máquina imitar comportamento humano em texto",
                    "A precisão de algoritmos de busca",
                    "A eficiência de redes neurais",
                ],
            ),
            DiagnosticQuestion(
                id="a01q3",
                question="Qual é um exemplo de IA fraca (narrow AI)?",
                options=[
                    "Uma IA que resolve qualquer problema cognitivo",
                    "Um sistema de recomendação de filmes",
                    "Uma IA com consciência própria",
                    "Robôs com inteligência geral",
                ],
            ),
        ],
        "answers": {
            "a01q1": "Sistemas que simulam capacidades cognitivas humanas",
            "a01q2": "A capacidade de uma máquina imitar comportamento humano em texto",
            "a01q3": "Um sistema de recomendação de filmes",
        },
        "weakness_map": {
            "a01q1": "Definição de IA",
            "a01q2": "Teste de Turing",
            "a01q3": "IA fraca vs IA geral",
        },
    },
    "aula02": {
        "title": "Diagnóstico — Agentes Inteligentes",
        "questions": [
            DiagnosticQuestion(
                id="a02q1",
                question="O que define um agente racional?",
                options=[
                    "Age para maximizar sua medida de desempenho dada a percepção e conhecimento",
                    "Sempre toma a decisão ótima independentemente do ambiente",
                    "Processa informações mais rápido que humanos",
                    "Nunca comete erros",
                ],
            ),
            DiagnosticQuestion(
                id="a02q2",
                question="Qual é a sequência correta de funcionamento de um agente?",
                options=[
                    "Ação → Percepção → Decisão",
                    "Percepção → Decisão → Ação",
                    "Decisão → Percepção → Ação",
                    "Ação → Decisão → Percepção",
                ],
            ),
            DiagnosticQuestion(
                id="a02q3",
                question="Um ambiente totalmente observável significa que:",
                options=[
                    "O agente pode ver o futuro",
                    "O agente tem acesso ao estado completo do ambiente a cada momento",
                    "O ambiente nunca muda",
                    "Existe apenas um agente no ambiente",
                ],
            ),
        ],
        "answers": {
            "a02q1": "Age para maximizar sua medida de desempenho dada a percepção e conhecimento",
            "a02q2": "Percepção → Decisão → Ação",
            "a02q3": "O agente tem acesso ao estado completo do ambiente a cada momento",
        },
        "weakness_map": {
            "a02q1": "Racionalidade de agentes",
            "a02q2": "Ciclo percepção-ação",
            "a02q3": "Tipos de ambiente",
        },
    },
    "aula03": {
        "title": "Diagnóstico — Busca e Otimização",
        "questions": [
            DiagnosticQuestion(
                id="a03q1",
                question="Qual algoritmo usa fila FIFO?",
                options=["DFS", "BFS", "Minimax", "Hill Climbing"],
            ),
            DiagnosticQuestion(
                id="a03q2",
                question="BFS garante encontrar o caminho mais curto quando:",
                options=[
                    "Todos os custos de aresta são iguais",
                    "O grafo não tem ciclos",
                    "A heurística é admissível",
                    "O espaço de estados é finito",
                ],
            ),
            DiagnosticQuestion(
                id="a03q3",
                question="O algoritmo A* usa qual critério de avaliação?",
                options=["g(n)", "h(n)", "f(n) = g(n) + h(n)", "f(n) = g(n) - h(n)"],
            ),
            DiagnosticQuestion(
                id="a03q4",
                question="Uma heurística admissível:",
                options=[
                    "Superestima o custo real",
                    "Nunca superestima o custo real",
                    "É sempre igual ao custo real",
                    "Sempre subestima em pelo menos 50%",
                ],
            ),
        ],
        "answers": {
            "a03q1": "BFS",
            "a03q2": "Todos os custos de aresta são iguais",
            "a03q3": "f(n) = g(n) + h(n)",
            "a03q4": "Nunca superestima o custo real",
        },
        "weakness_map": {
            "a03q1": "Estrutura de dados do BFS",
            "a03q2": "Completude e otimalidade do BFS",
            "a03q3": "Função de avaliação A*",
            "a03q4": "Heurísticas admissíveis",
        },
    },
    "aula04": {
        "title": "Diagnóstico — Busca Local e Adversarial",
        "questions": [
            DiagnosticQuestion(
                id="a04q1",
                question="Hill Climbing pode ficar preso em:",
                options=[
                    "Ótimos globais",
                    "Ótimos locais, platôs e cristas",
                    "Grafos desconexos",
                    "Heurísticas inadmissíveis",
                ],
            ),
            DiagnosticQuestion(
                id="a04q2",
                question="No Minimax, o jogador MIN tenta:",
                options=[
                    "Maximizar o valor para ambos os jogadores",
                    "Minimizar o valor para o jogador MAX",
                    "Encontrar o caminho mais curto",
                    "Maximizar seu próprio valor",
                ],
            ),
            DiagnosticQuestion(
                id="a04q3",
                question="A poda alfa-beta:",
                options=[
                    "Muda o resultado do Minimax",
                    "Elimina ramos que não afetam a decisão final",
                    "Aumenta a profundidade de busca",
                    "Substitui a função heurística",
                ],
            ),
        ],
        "answers": {
            "a04q1": "Ótimos locais, platôs e cristas",
            "a04q2": "Minimizar o valor para o jogador MAX",
            "a04q3": "Elimina ramos que não afetam a decisão final",
        },
        "weakness_map": {
            "a04q1": "Limitações do Hill Climbing",
            "a04q2": "Estratégia MIN no Minimax",
            "a04q3": "Poda alfa-beta",
        },
    },
    "aula05": {
        "title": "Diagnóstico — Representação do Conhecimento",
        "questions": [
            DiagnosticQuestion(
                id="a05q1",
                question="RAG (Retrieval-Augmented Generation) combina:",
                options=[
                    "Banco relacional com aprendizado supervisionado",
                    "Recuperação de informação com geração de texto por LLM",
                    "Redes neurais com regras lógicas",
                    "Busca em grafos com clustering",
                ],
            ),
            DiagnosticQuestion(
                id="a05q2",
                question="Em lógica proposicional, a sentença 'P → Q' é falsa quando:",
                options=[
                    "P é falso e Q é verdadeiro",
                    "P é verdadeiro e Q é falso",
                    "P e Q são ambos verdadeiros",
                    "P e Q são ambos falsos",
                ],
            ),
            DiagnosticQuestion(
                id="a05q3",
                question="Um embedding é:",
                options=[
                    "Um arquivo comprimido",
                    "Uma representação numérica vetorial de texto",
                    "Um tipo de banco de dados",
                    "Um algoritmo de busca",
                ],
            ),
        ],
        "answers": {
            "a05q1": "Recuperação de informação com geração de texto por LLM",
            "a05q2": "P é verdadeiro e Q é falso",
            "a05q3": "Uma representação numérica vetorial de texto",
        },
        "weakness_map": {
            "a05q1": "RAG",
            "a05q2": "Lógica proposicional",
            "a05q3": "Embeddings",
        },
    },
    "aula06": {
        "title": "Diagnóstico — ML Supervisionado",
        "questions": [
            DiagnosticQuestion(
                id="a06q1",
                question="Overfitting ocorre quando:",
                options=[
                    "O modelo tem baixa acurácia no treino e no teste",
                    "O modelo performa bem no treino mas mal em dados novos",
                    "O modelo não converge durante o treinamento",
                    "Os dados de treino são insuficientes",
                ],
            ),
            DiagnosticQuestion(
                id="a06q2",
                question="Qual métrica é mais adequada para classificação com classes desbalanceadas?",
                options=["Acurácia", "F1-Score", "MSE", "R²"],
            ),
            DiagnosticQuestion(
                id="a06q3",
                question="Regressão linear modela a relação entre variáveis como:",
                options=[
                    "Uma curva exponencial",
                    "Uma função linear y = ax + b",
                    "Uma árvore de decisão",
                    "Um cluster de pontos",
                ],
            ),
        ],
        "answers": {
            "a06q1": "O modelo performa bem no treino mas mal em dados novos",
            "a06q2": "F1-Score",
            "a06q3": "Uma função linear y = ax + b",
        },
        "weakness_map": {
            "a06q1": "Overfitting",
            "a06q2": "Métricas de classificação",
            "a06q3": "Regressão linear",
        },
    },
    "aula07": {
        "title": "Diagnóstico — Clustering e Ensembles",
        "questions": [
            DiagnosticQuestion(
                id="a07q1",
                question="K-means é um algoritmo de:",
                options=[
                    "Classificação supervisionada",
                    "Clustering não supervisionado",
                    "Regressão",
                    "Busca em grafos",
                ],
            ),
            DiagnosticQuestion(
                id="a07q2",
                question="Random Forest é composto por:",
                options=[
                    "Múltiplas redes neurais",
                    "Um conjunto de árvores de decisão independentes",
                    "Vários algoritmos K-means",
                    "Uma única árvore de decisão profunda",
                ],
            ),
            DiagnosticQuestion(
                id="a07q3",
                question="Bagging reduz principalmente:",
                options=["Bias", "Variância", "Tempo de treinamento", "Número de features"],
            ),
        ],
        "answers": {
            "a07q1": "Clustering não supervisionado",
            "a07q2": "Um conjunto de árvores de decisão independentes",
            "a07q3": "Variância",
        },
        "weakness_map": {
            "a07q1": "K-means",
            "a07q2": "Random Forest",
            "a07q3": "Técnica de Bagging",
        },
    },
}


def get_quiz(topic_id: str) -> DiagnosticQuizResponse:
    data = _QUIZZES.get(topic_id)
    if not data:
        raise TopicNotFoundError(topic_id)
    return DiagnosticQuizResponse(
        topic_id=topic_id,
        title=data["title"],
        questions=data["questions"],
    )


def submit(req: DiagnosticSubmitRequest) -> DiagnosticResult:
    data = _QUIZZES.get(req.topic_id)
    if not data:
        raise TopicNotFoundError(req.topic_id)

    answers = data["answers"]
    weakness_map = data["weakness_map"]

    score = 0
    weaknesses: list[str] = []
    for ans in req.answers:
        if answers.get(ans.question_id) == ans.selected_option:
            score += 1
        elif ans.question_id in weakness_map:
            weaknesses.append(weakness_map[ans.question_id])

    if not weaknesses:
        recommendation = "Ótimo desempenho! Continue revisando os conceitos para consolidar o aprendizado."
    else:
        recommendation = (
            f"Revise os seguintes tópicos: {', '.join(weaknesses)}. "
            "Consulte o tutor para esclarecer dúvidas."
        )

    return DiagnosticResult(
        score=score,
        total=len(req.answers),
        weaknesses=weaknesses,
        recommendation=recommendation,
    )
