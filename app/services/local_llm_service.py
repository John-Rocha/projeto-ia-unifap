"""
Substituição local do llm_service.
Implementa loop ReAct com uma ferramenta: buscar_disciplina().
Sem chamadas externas — geração determinística baseada nos chunks recuperados.
"""
from app.services.local_retrieval_service import search


# ─── Ferramentas disponíveis para o agente ───

def _buscar_disciplina(query: str) -> str:
    matches = search(query, top_k=3)
    if not matches or matches[0].score == 0.0:
        return "Nenhum trecho relevante encontrado no material."
    parts = []
    for m in matches:
        aula = m.metadata.get("aula", "?")
        titulo = m.metadata.get("titulo_aula", "")
        texto = m.metadata.get("text", "")[:600]
        score = round(m.score, 3)
        parts.append(f"[{aula} · {titulo} · score={score}] {texto}")
    return "\n\n".join(parts)


_FERRAMENTAS = {"buscar_disciplina": _buscar_disciplina}


# ─── Loop ReAct ───

def _react(objetivo: str) -> tuple[str, list[dict]]:
    """
    Ciclo ReAct:
      1. Pensamento: o que preciso buscar?
      2. Ação: chamar buscar_disciplina(query)
      3. Observação: resultado da busca
      4. Resposta: montar resposta com base na observação
    Retorna (resposta_texto, log_do_ciclo)
    """
    log = []

    # Extrair a pergunta real do prompt (após "Pergunta do aluno:")
    query = objetivo
    if "Pergunta do aluno:" in objetivo:
        query = objetivo.split("Pergunta do aluno:")[-1].strip().split("\n")[0].strip()

    # Passo 1 — Pensamento
    pensamento = f"Preciso buscar no material da disciplina sobre: '{query}'"
    log.append({"tipo": "Pensamento", "conteudo": pensamento})

    # Passo 2 — Ação
    resultado_busca = _FERRAMENTAS["buscar_disciplina"](query)
    log.append({"tipo": "Ação", "ferramenta": "buscar_disciplina", "arg": query})
    log.append({"tipo": "Observação", "conteudo": resultado_busca})

    # Passo 3 — Resposta
    if "Nenhum trecho" in resultado_busca:
        resposta = (
            "Não encontrei informação suficiente no material da disciplina para responder "
            "com segurança. Tente reformular a pergunta ou pergunte sobre outro tópico."
        )
    else:
        # Pega o primeiro trecho como base da resposta
        # Formato: [aula01 · Titulo da Aula · score=0.091] texto...
        primeiro = resultado_busca.split("\n\n")[0]
        aula = "?"
        titulo = ""
        texto_trecho = primeiro
        if primeiro.startswith("["):
            header, _, corpo = primeiro.partition("] ")
            partes = header.lstrip("[").split(" · ")
            aula = partes[0] if len(partes) > 0 else "?"
            titulo = partes[1] if len(partes) > 1 else ""
            texto_trecho = corpo.strip()

        ref = f"{titulo} ({aula})" if titulo else aula
        resposta = (
            f"Com base no material da disciplina — {ref}:\n\n"
            f"{texto_trecho}"
        )

    log.append({"tipo": "Resposta", "conteudo": resposta})
    return resposta, log


def generate(prompt: str) -> str:
    """
    Interface pública idêntica a llm_service.generate().
    Recebe prompt completo (com contexto RAG) e retorna resposta como string.
    """
    resposta, _ = _react(prompt)
    return resposta
