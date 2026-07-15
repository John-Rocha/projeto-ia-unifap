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
            EmbSvc["embedding_service\n(OpenAI)"]
            PinSvc["pinecone_service\n(busca vetorial)"]
            LLMSvc["llm_service\n(GPT-4o-mini)"]
            StudySvc["local_study_plan_service\n(determinístico)"]
        end
    end

    subgraph External["APIs Externas"]
        OpenAI["OpenAI API\n(embeddings + chat)"]
        Pinecone["Pinecone\n(índice vetorial)"]
    end

    Ingest["ingest_openai.py\n(script de ingestão)"]
    HTML["docs/Aula_*.html\n(8 arquivos)"]

    Home -->|GET| Topics
    Quiz -->|GET quiz / POST submit| DiagAPI
    Chat -->|POST| ChatAPI
    Plan -->|POST| PlanAPI

    ChatAPI --> RAGSvc
    DiagAPI --> DiagSvc
    PlanAPI --> PlanSvc
    RAGSearch --> EmbSvc

    RAGSvc --> EmbSvc
    RAGSvc --> PinSvc
    RAGSvc --> LLMSvc
    PlanSvc --> StudySvc

    EmbSvc --> OpenAI
    LLMSvc --> OpenAI
    PinSvc --> Pinecone

    HTML --> Ingest
    Ingest --> OpenAI
    Ingest --> Pinecone
```

### Fluxo do chat (RAG com OpenAI + Pinecone)

```mermaid
sequenceDiagram
    actor Aluno
    participant FE as Frontend
    participant BE as Backend
    participant OAI as OpenAI API
    participant PIN as Pinecone

    Aluno->>FE: digita pergunta
    FE->>BE: POST /api/v1/chat {question}
    BE->>OAI: embeddings.create(question) → vetor 512d
    OAI-->>BE: vetor semântico
    BE->>PIN: index.query(vector, top_k=5)
    PIN-->>BE: top-k chunks com scores de similaridade cosseno
    BE->>BE: monta prompt com contexto dos chunks
    BE->>OAI: chat.completions.create(gpt-4o-mini, prompt)
    OAI-->>BE: resposta em linguagem natural
    BE-->>FE: {answer, sources, confidence}
    FE-->>Aluno: exibe resposta + fontes (aula + score)
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
- 8 aulas da disciplina exibidas em cards (Panorama da IA até Tópicos Modernos: LLMs, RAG e Agentes).
- Cada card tem atalho direto para o quiz diagnóstico e para o chat filtrado pela aula.

### Quiz diagnóstico (`/diagnostic/[id]`)
- 3 a 4 questões de múltipla escolha por aula.
- Após submissão: score, porcentagem de acerto e lista de tópicos com dificuldade.
- Botão para gerar plano de estudos com base nas fraquezas identificadas.

### Chat com o tutor (`/chat`)
- Pergunta livre em linguagem natural.
- Recuperação semântica via OpenAI Embeddings (`text-embedding-3-small`) + Pinecone.
- Resposta gerada por `gpt-4o-mini` com contexto dos chunks recuperados.
- Exibe fonte (aula + título) e score de similaridade cosseno por chunk.

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

> Também necessário: conta na **OpenAI** (para embeddings e GPT-4o-mini) e conta no **Pinecone** (índice vetorial, plano free suficiente).

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

### 3. Configurar variáveis de ambiente

Copie o arquivo de exemplo e preencha as chaves:

```bash
cp .env.example .env
```

Edite `.env` com suas chaves:

```env
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
PINECONE_HOST=https://seu-index.svc.aped-xxxx.pinecone.io
```

> `PINECONE_HOST` é a URL do seu índice no painel do Pinecone. Crie um índice com dimensão **512** e métrica **cosine**.

### 4. Ingestão (primeira vez)

Extrai os HTMLs das aulas, gera embeddings e envia ao Pinecone:

```bash
python ingest_openai.py
```

~67 chunks de 8 aulas. Leva alguns minutos (rate limit OpenAI). Execute novamente apenas se o material mudar.

### 5. Iniciar o backend

```bash
python run.py
```

API disponível em `http://localhost:8000`.
Documentação interativa em `http://localhost:8000/docs`.

### 6. Frontend (Next.js)

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
| `python ingest_openai.py` | Gera embeddings dos HTMLs e envia ao Pinecone |
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
│   │   ├── rag_service.py              # Orquestra embed → query → generate
│   │   ├── embedding_service.py        # OpenAI text-embedding-3-small
│   │   ├── pinecone_service.py         # Busca vetorial no Pinecone
│   │   ├── llm_service.py              # GPT-4o-mini para geração de respostas
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
├── docs/                       # Slides das aulas em HTML (Aula_01 a Aula_08)
├── relatorio/                  
│   ├── relatorio_tecnico.pdf   # Relatório técnico do projeto
├── ingest_openai.py            # Ingestão: HTML → embeddings → Pinecone
├── run.py                      # Entry point do backend
├── requirements.txt
└── .env.example
```

---

## Tecnologias

**Backend:** FastAPI · Pydantic · Uvicorn

**Frontend:** Next.js 16 · React 19 · TypeScript · Tailwind CSS 4

**IA e busca:**
- OpenAI `text-embedding-3-small` (512d) — embeddings semânticos dos chunks
- Pinecone — índice vetorial com similaridade cosseno
- OpenAI `gpt-4o-mini` — geração de respostas em linguagem natural
- Planejador determinístico — mapa fraqueza → passos de estudo (sem LLM)
