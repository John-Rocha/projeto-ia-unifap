# TutorIA — CC0121 Inteligência Artificial

Tutor inteligente para a disciplina **CC0121 — Inteligência Artificial** da UNIFAP.
Combina RAG (Retrieval-Augmented Generation) com um frontend Next.js para oferecer chat com tutor, quiz diagnóstico por aula e plano de estudos personalizado.

**Equipe:** Evelyn Santos · Johnathan Rocha · Aymmée Diniz

---

## Arquitetura

### Visão geral dos componentes

```mermaid
graph TB
    subgraph Frontend["Frontend — Next.js 16 (tutoria/)"]
        Home["/ — Lista de aulas"]
        Quiz["/diagnostic/[id] — Quiz"]
        Chat["/chat — Chat com tutor"]
        Plan["/study-plan — Plano de estudos"]
    end

    subgraph Backend["Backend — FastAPI (app/)"]
        Topics["GET /api/v1/topics"]
        ChatAPI["POST /api/v1/chat"]
        DiagAPI["GET|POST /api/v1/diagnostic/*"]
        PlanAPI["POST /api/v1/study-plan"]
        RAGSearch["POST /api/v1/rag/search"]

        subgraph Services["Services"]
            RAGSvc["rag_service"]
            DiagSvc["diagnostic_service"]
            PlanSvc["study_plan_service"]
            RetrSvc["local_retrieval_service\n(Jaccard)"]
            LLMSvc["local_llm_service\n(ReAct)"]
            StudySvc["local_study_plan_service\n(determinístico)"]
        end
    end

    subgraph Local["Algoritmos locais — sem API externa"]
        Jaccard["Similaridade de Jaccard\n(recuperação léxica)"]
        ReAct["Loop ReAct\n(geração determinística)"]
        Tiktoken["Tiktoken cl100k_base\n(chunking por tokens)"]
    end

    Ingest["ingest_local.py\n(script de ingestão)"]
    PDF["data/disciplina_ia.pdf"]
    Chunks["data/chunks.json"]

    Home -->|GET| Topics
    Quiz -->|GET quiz / POST submit| DiagAPI
    Chat -->|POST| ChatAPI
    Plan -->|POST| PlanAPI

    ChatAPI --> RAGSvc
    DiagAPI --> DiagSvc
    PlanAPI --> PlanSvc
    RAGSearch --> RetrSvc

    RAGSvc --> RetrSvc
    RAGSvc --> LLMSvc
    PlanSvc --> StudySvc

    RetrSvc --> Jaccard
    LLMSvc --> ReAct
    LLMSvc --> RetrSvc

    PDF --> Ingest
    Ingest --> Tiktoken
    Ingest --> Chunks
    RetrSvc --> Chunks
```

### Fluxo do chat (RAG local)

```mermaid
sequenceDiagram
    actor Aluno
    participant FE as Frontend
    participant BE as Backend
    participant RET as local_retrieval_service
    participant LLM as local_llm_service

    Aluno->>FE: digita pergunta
    FE->>BE: POST /api/v1/chat {question}
    BE->>RET: search(question, top_k=5)
    RET->>RET: Jaccard(question, chunk) para cada chunk em chunks.json
    RET-->>BE: top-k chunks com scores
    BE->>BE: monta prompt com contexto dos chunks
    BE->>LLM: generate(prompt)
    LLM->>LLM: ReAct — Pensamento → buscar_disciplina() → Observação → Resposta
    LLM-->>BE: resposta baseada no chunk mais relevante
    BE-->>FE: {answer, sources, confidence}
    FE-->>Aluno: exibe resposta + fontes (página + score)
```

### Fluxo do diagnóstico → plano de estudos

```mermaid
sequenceDiagram
    actor Aluno
    participant FE as Frontend
    participant BE as Backend
    participant Plan as local_study_plan_service

    Aluno->>FE: seleciona aula
    FE->>BE: GET /api/v1/diagnostic/quiz?topic_id=aula01
    BE-->>FE: {title, questions[]}
    FE-->>Aluno: exibe questões

    Aluno->>FE: responde e envia
    FE->>BE: POST /api/v1/diagnostic/submit {answers[]}
    BE->>BE: corrige respostas, mapeia fraquezas
    BE-->>FE: {score, weaknesses[]}
    FE-->>Aluno: exibe resultado

    Aluno->>FE: clica "Gerar plano de estudos"
    FE->>BE: POST /api/v1/study-plan {weaknesses[]}
    BE->>Plan: generate_plan(weaknesses)
    Plan->>Plan: mapeia fraqueza → StudyStep pré-definido
    Plan-->>BE: {title, steps[]}
    BE-->>FE: {title, steps[]}
    FE-->>Aluno: exibe plano ordenado
```

---

## Funcionalidades

### Home — lista de aulas
- 7 aulas da disciplina exibidas em cards.
- Cada card tem atalho direto para o quiz diagnóstico e para o chat filtrado pela aula.

### Quiz diagnóstico (`/diagnostic/[id]`)
- 3 a 4 questões de múltipla escolha por aula.
- Após submissão: score, porcentagem de acerto e lista de tópicos com dificuldade.
- Botão para gerar plano de estudos com base nas fraquezas identificadas.

### Chat com o tutor (`/chat`)
- Pergunta livre em linguagem natural.
- Recuperação por similaridade de Jaccard sobre os chunks do PDF da disciplina.
- Resposta gerada pelo loop ReAct com a ferramenta `buscar_disciplina()`.
- Exibe fonte (página do PDF) e score de similaridade por chunk.

### Plano de estudos (`/study-plan`)
- Gerado deterministicamente com base nas fraquezas do quiz.
- Passos ordenados do conteúdo mais fundamental ao mais avançado.
- Cada passo inclui tópico, descrição e referência à aula correspondente.

---

## Pré-requisitos

| Ferramenta | Versão mínima |
|---|---|
| Python | 3.12 |
| Node.js | 20 |
| npm | 10 |

> Nenhuma conta externa necessária. O sistema roda 100% offline.

---

## Instalação

### 1. Clonar o repositório

```bash
git clone <url-do-repo>
cd projeto-ia-unifap
```

### 2. Backend (FastAPI)

```bash
# Criar e ativar ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 3. Ingestão do PDF (primeira vez)

> Necessário apenas uma vez para gerar o arquivo de chunks local.

Coloque o PDF do material da disciplina em `data/disciplina_ia.pdf` e execute:

```bash
python ingest_local.py
```

O script usa **tiktoken** (encoder `cl100k_base`) para dividir o PDF em chunks de ~800 tokens com sobreposição de 100, salvando o resultado em `data/chunks.json`. Sem chamadas externas.

### 4. Iniciar o backend

```bash
python run.py
```

API disponível em `http://localhost:8000`.
Documentação interativa em `http://localhost:8000/docs`.

### 5. Frontend (Next.js)

```bash
cd tutoria

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento (porta 3000)
npm run dev
```

App disponível em `http://localhost:3000`.

> O frontend lê a URL do backend via `NEXT_PUBLIC_API_URL`. O arquivo `tutoria/.env.local` já vem configurado para `http://localhost:8000/api/v1`.

---

## Scripts úteis

| Comando | Descrição |
|---|---|
| `python ingest_local.py` | Processa PDF e salva chunks em `data/chunks.json` |
| `python run.py` | Inicia o backend com hot-reload |
| `cd tutoria && npm run dev` | Inicia o frontend em dev |
| `cd tutoria && npm run build` | Build de produção do frontend |

---

## Estrutura de pastas

```
projeto-ia-unifap/
├── app/                        # Backend FastAPI
│   ├── api/
│   │   ├── routes/             # Endpoints (chat, diagnostic, rag, study-plan, topics)
│   │   └── schemas/            # Modelos Pydantic de request/response
│   ├── core/
│   │   ├── config.py           # Configurações via pydantic-settings
│   │   └── exceptions.py       # Exceções customizadas
│   ├── services/               # Lógica de negócio
│   │   ├── rag_service.py      # Orquestra recuperação + geração
│   │   ├── local_retrieval_service.py  # Jaccard similarity sobre chunks.json
│   │   ├── local_llm_service.py        # Loop ReAct com buscar_disciplina()
│   │   ├── local_study_plan_service.py # Planejador determinístico
│   │   ├── diagnostic_service.py
│   │   └── study_plan_service.py
│   └── utils/
│       └── prompt_builder.py
├── tutoria/                    # Frontend Next.js
│   ├── app/
│   │   ├── page.tsx            # Home — lista de aulas
│   │   ├── chat/page.tsx       # Chat com o tutor
│   │   ├── diagnostic/[id]/    # Quiz diagnóstico
│   │   └── study-plan/         # Plano de estudos
│   └── lib/
│       └── api.ts              # Cliente tipado para a API REST
├── data/
│   ├── disciplina_ia.pdf       # Material da disciplina (necessário para ingestão)
│   └── chunks.json             # Chunks gerados por ingest_local.py
├── docs/                       # Slides e materiais das aulas (HTML)
├── ingest_local.py             # Script de ingestão — tiktoken, salva chunks.json
├── run.py                      # Entry point do backend
├── requirements.txt
└── .env.example
```

---

## Tecnologias

**Backend:** FastAPI · Pydantic · Uvicorn

**Frontend:** Next.js 16 · React 19 · TypeScript · Tailwind CSS 4

**Algoritmos de IA (locais):**
- `tiktoken` (cl100k_base) — chunking do PDF por tokens
- Similaridade de Jaccard — recuperação léxica de chunks relevantes
- Loop ReAct — agente com ferramenta de busca para geração de respostas
- Planejador determinístico — mapa fraqueza → passos de estudo
