# PRD — Backend TutorIA CC0121

## 1. Visão Geral

O backend do **TutorIA CC0121** será desenvolvido em **FastAPI** e terá como principal responsabilidade permitir que o frontend em Flutter consulte um tutor inteligente baseado nos conteúdos da disciplina de Inteligência Artificial.

O fluxo definido para o projeto é:

```text
PDF com o conteúdo da disciplina
        ↓
Processamento e vetorização do conteúdo
        ↓
Armazenamento dos embeddings no Pinecone
        ↓
Consulta RAG no Pinecone
        ↓
Geração da resposta pelo LLM
        ↓
Retorno da resposta para o Flutter
```

Neste modelo, o **Pinecone será o banco vetorial principal**. O PDF da disciplina será previamente processado e usado para alimentar o Pinecone. Durante a execução do sistema, o backend não consultará diretamente o PDF; ele consultará os vetores e metadados armazenados no Pinecone.

---

## 2. Objetivo do Backend

Construir uma API em FastAPI capaz de:

- receber perguntas enviadas pelo frontend Flutter;
- gerar embedding da pergunta do usuário;
- consultar o Pinecone para recuperar os trechos mais relevantes do conteúdo da disciplina;
- montar um contexto para o modelo de linguagem;
- gerar uma resposta baseada nos trechos recuperados;
- retornar resposta, fontes e metadados ao frontend;
- disponibilizar endpoints de diagnóstico e plano de estudo;
- manter uma arquitetura simples, funcional e adequada para demonstração em sala de aula.

---

## 3. Escopo do Backend

### 3.1 Dentro do escopo

- API REST em FastAPI.
- Integração com Pinecone.
- Consulta RAG sobre os vetores armazenados no Pinecone.
- Geração de embeddings da pergunta do usuário.
- Geração de resposta com LLM.
- Retorno das fontes utilizadas na resposta.
- Endpoints para chat, temas, diagnóstico e plano de estudo.
- Script de ingestão do PDF para Pinecone.
- Configuração via variáveis de ambiente.
- Documentação automática via Swagger/OpenAPI.

### 3.2 Fora do escopo

- Login/autenticação de usuários.
- Controle de permissões.
- Pagamento ou assinatura.
- Deploy em produção.
- Aplicativo mobile publicado em loja.
- Treinamento próprio de modelo de linguagem.
- Fine-tuning de LLM.
- Banco relacional para histórico completo de usuários.

---

## 4. Fluxo Funcional Principal

### 4.1 Fluxo de ingestão do PDF

Este fluxo será executado antes da demonstração do sistema.

```text
1. O PDF da disciplina é colocado em uma pasta local.
2. Um script Python extrai o texto do PDF.
3. O texto é dividido em chunks.
4. Cada chunk recebe metadados, como aula, tema, página e índice.
5. O sistema gera embeddings para cada chunk.
6. Os embeddings são enviados para o Pinecone.
7. O Pinecone passa a ser a base de consulta do RAG.
```

### 4.2 Fluxo de pergunta e resposta

```text
1. O aluno digita uma pergunta no app Flutter.
2. O Flutter envia a pergunta para o backend FastAPI.
3. O backend gera o embedding da pergunta.
4. O backend consulta o Pinecone.
5. O Pinecone retorna os chunks mais relevantes.
6. O backend monta o prompt com os chunks recuperados.
7. O LLM gera uma resposta com base no contexto.
8. O backend retorna ao Flutter:
   - resposta;
   - fonte;
   - trechos utilizados;
   - tema/aula relacionada;
   - nível de confiança aproximado.
```

---

## 5. Arquitetura Técnica

```text
Flutter Web
    ↓ HTTP
FastAPI
    ↓
Chat Service
    ↓
RAG Service
    ↓
Embedding Service
    ↓
Pinecone Vector Database
    ↓
Chunks vetorizados do PDF
    ↓
LLM Service
    ↓
Resposta fundamentada
```

---

## 6. Componentes do Backend

### 6.1 FastAPI App

Responsável por expor os endpoints HTTP utilizados pelo frontend.

Principais responsabilidades:

- receber requisições;
- validar payloads com Pydantic;
- acionar os serviços internos;
- retornar respostas padronizadas;
- expor documentação Swagger.

### 6.2 RAG Service

Responsável por coordenar o fluxo de recuperação aumentada por geração.

Responsabilidades:

- receber a pergunta do usuário;
- gerar embedding da pergunta;
- consultar o Pinecone;
- recuperar os chunks mais relevantes;
- montar o contexto do prompt;
- chamar o LLM;
- retornar resposta estruturada.

### 6.3 Pinecone Service

Responsável por toda comunicação com o Pinecone.

Responsabilidades:

- conectar ao índice configurado;
- realizar upsert dos vetores no fluxo de ingestão;
- realizar consultas vetoriais no fluxo RAG;
- aplicar filtros por metadados, quando informados;
- retornar chunks ordenados por similaridade.

### 6.4 Embedding Service

Responsável por gerar vetores numéricos a partir de texto.

Responsabilidades:

- gerar embeddings dos chunks do PDF;
- gerar embedding da pergunta do usuário;
- garantir compatibilidade entre o modelo de embedding e a dimensão do índice Pinecone.

### 6.5 LLM Service

Responsável pela comunicação com o modelo de linguagem.

Responsabilidades:

- receber pergunta e contexto;
- montar prompt final;
- gerar resposta clara e didática;
- evitar respostas fora do contexto recuperado;
- informar quando o conteúdo não estiver presente na base.

### 6.6 Diagnostic Service

Responsável por gerar ou retornar perguntas de diagnóstico por tema.

Responsabilidades:

- disponibilizar quizzes por tema;
- corrigir respostas;
- identificar lacunas de aprendizagem;
- retornar recomendações iniciais.

### 6.7 Study Plan Service

Responsável por gerar trilhas de estudo com base nas lacunas identificadas.

Responsabilidades:

- receber lista de dificuldades;
- mapear pré-requisitos;
- montar plano de estudo em ordem lógica;
- retornar tópicos e justificativas.

---

## 7. Estrutura de Pastas Sugerida

```text
backend/
 ├── app/
 │   ├── main.py
 │   ├── core/
 │   │   ├── config.py
 │   │   └── exceptions.py
 │   │
 │   ├── api/
 │   │   ├── routes/
 │   │   │   ├── chat_routes.py
 │   │   │   ├── topic_routes.py
 │   │   │   ├── diagnostic_routes.py
 │   │   │   └── study_plan_routes.py
 │   │   └── schemas/
 │   │       ├── chat_schema.py
 │   │       ├── diagnostic_schema.py
 │   │       └── study_plan_schema.py
 │   │
 │   ├── services/
 │   │   ├── rag_service.py
 │   │   ├── pinecone_service.py
 │   │   ├── embedding_service.py
 │   │   ├── llm_service.py
 │   │   ├── diagnostic_service.py
 │   │   └── study_plan_service.py
 │   │
 │   ├── scripts/
 │   │   ├── ingest_pdf_to_pinecone.py
 │   │   └── clear_pinecone_index.py
 │   │
 │   └── utils/
 │       ├── pdf_loader.py
 │       ├── text_splitter.py
 │       └── prompt_builder.py
 │
 ├── data/
 │   └── disciplina_ia.pdf
 │
 ├── tests/
 │   ├── test_chat.py
 │   ├── test_rag.py
 │   └── test_diagnostic.py
 │
 ├── .env.example
 ├── requirements.txt
 ├── README.md
 └── run.py
```

---

## 8. Variáveis de Ambiente

```env
APP_NAME=TutorIA CC0121 Backend
APP_ENV=development
API_PREFIX=/api/v1

PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=tutoria-cc0121
PINECONE_NAMESPACE=disciplina-ia

EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSION=1536

LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.2

CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8080
```

---

## 9. Metadados dos Chunks no Pinecone

Cada chunk armazenado no Pinecone deve conter metadados suficientes para rastrear a origem da resposta.

Exemplo:

```json
{
  "id": "aula03_pagina012_chunk004",
  "values": [0.012, -0.034, 0.087],
  "metadata": {
    "text": "BFS explora os nós em largura usando fila FIFO...",
    "aula": "Aula 03",
    "titulo_aula": "Busca e Otimização",
    "tema": "Busca",
    "topico": "BFS",
    "pagina": 12,
    "chunk_index": 4,
    "source": "disciplina_ia.pdf"
  }
}
```

Campos obrigatórios:

| Campo | Descrição |
|---|---|
| `text` | Texto original do chunk |
| `aula` | Número ou identificação da aula |
| `titulo_aula` | Título da aula |
| `tema` | Tema principal do trecho |
| `pagina` | Página do PDF |
| `chunk_index` | Índice do chunk |
| `source` | Nome do arquivo de origem |

---

## 10. Endpoints da API

### 10.1 Health Check

```http
GET /api/v1/health
```

#### Response

```json
{
  "status": "ok",
  "service": "TutorIA CC0121 Backend"
}
```

---

### 10.2 Listar Temas

```http
GET /api/v1/topics
```

#### Response

```json
{
  "topics": [
    {
      "id": "aula03",
      "title": "Busca e Otimização",
      "description": "BFS, DFS, A* e heurísticas"
    },
    {
      "id": "aula05",
      "title": "Representação do Conhecimento",
      "description": "Lógica, sistemas especialistas, grafos e RAG"
    }
  ]
}
```

---

### 10.3 Perguntar ao Tutor

```http
POST /api/v1/chat
```

#### Request

```json
{
  "question": "Qual a diferença entre BFS e DFS?",
  "topic_id": "aula03",
  "top_k": 5
}
```

#### Response

```json
{
  "answer": "BFS explora os nós em largura usando uma fila FIFO. DFS explora em profundidade usando uma pilha LIFO. Quando todos os custos são iguais, BFS garante o menor caminho, enquanto DFS não garante.",
  "sources": [
    {
      "aula": "Aula 03",
      "titulo_aula": "Busca e Otimização",
      "pagina": 8,
      "topico": "BFS",
      "score": 0.91
    },
    {
      "aula": "Aula 03",
      "titulo_aula": "Busca e Otimização",
      "pagina": 10,
      "topico": "DFS",
      "score": 0.88
    }
  ],
  "retrieved_chunks": [
    "BFS explora nível por nível...",
    "DFS vai o mais fundo possível antes de voltar..."
  ],
  "confidence": 0.89
}
```

---

### 10.4 Buscar Chunks no Pinecone

Endpoint útil para teste técnico e debug.

```http
POST /api/v1/rag/search
```

#### Request

```json
{
  "query": "explique busca em largura",
  "topic_id": "aula03",
  "top_k": 5
}
```

#### Response

```json
{
  "matches": [
    {
      "text": "BFS explora nível por nível...",
      "score": 0.92,
      "metadata": {
        "aula": "Aula 03",
        "titulo_aula": "Busca e Otimização",
        "pagina": 8,
        "topico": "BFS"
      }
    }
  ]
}
```

---

### 10.5 Obter Quiz de Diagnóstico

```http
GET /api/v1/diagnostic/quiz?topic_id=aula03
```

#### Response

```json
{
  "topic_id": "aula03",
  "title": "Diagnóstico — Busca e Otimização",
  "questions": [
    {
      "id": "q1",
      "question": "Qual algoritmo usa fila FIFO?",
      "options": ["DFS", "BFS", "Minimax", "Hill Climbing"]
    }
  ]
}
```

---

### 10.6 Corrigir Diagnóstico

```http
POST /api/v1/diagnostic/submit
```

#### Request

```json
{
  "topic_id": "aula03",
  "answers": [
    {
      "question_id": "q1",
      "selected_option": "DFS"
    }
  ]
}
```

#### Response

```json
{
  "score": 0,
  "total": 1,
  "weaknesses": ["BFS", "Estruturas de dados em busca"],
  "recommendation": "Revise busca em largura, principalmente o uso de fila FIFO e a diferença em relação à DFS."
}
```

---

### 10.7 Gerar Plano de Estudo

```http
POST /api/v1/study-plan
```

#### Request

```json
{
  "weaknesses": ["BFS", "DFS", "Heurísticas"],
  "goal": "Revisar para a prova"
}
```

#### Response

```json
{
  "title": "Plano de Estudo Personalizado",
  "steps": [
    {
      "order": 1,
      "topic": "BFS",
      "description": "Revise busca em largura e a estrutura de fila FIFO.",
      "source": "Aula 03 — Busca e Otimização"
    },
    {
      "order": 2,
      "topic": "DFS",
      "description": "Compare DFS com BFS, observando pilha LIFO e ausência de garantia de menor caminho.",
      "source": "Aula 03 — Busca e Otimização"
    }
  ]
}
```

---

## 11. Requisitos Funcionais

### RF01 — Consultar o Tutor

O sistema deve permitir que o frontend envie uma pergunta e receba uma resposta gerada com base nos conteúdos recuperados do Pinecone.

### RF02 — Recuperar trechos relevantes

O sistema deve consultar o Pinecone usando embedding da pergunta e recuperar os chunks mais relevantes do PDF vetorizado.

### RF03 — Retornar fontes da resposta

O sistema deve retornar, junto com a resposta, os metadados dos chunks utilizados, como aula, página, tema e score de similaridade.

### RF04 — Filtrar por tema

O sistema deve permitir que a consulta seja filtrada por tema ou aula, quando o frontend enviar `topic_id`.

### RF05 — Informar ausência de contexto

O sistema deve informar quando a base recuperada não for suficiente para responder à pergunta.

### RF06 — Disponibilizar diagnóstico

O sistema deve disponibilizar quizzes simples por tema da disciplina.

### RF07 — Corrigir diagnóstico

O sistema deve corrigir as respostas do diagnóstico e indicar lacunas de conhecimento.

### RF08 — Gerar plano de estudo

O sistema deve gerar uma trilha de estudo com base nas lacunas identificadas.

### RF09 — Ingestão do PDF

O sistema deve disponibilizar script para processar o PDF, gerar chunks, criar embeddings e alimentar o Pinecone.

### RF10 — Health check

O sistema deve disponibilizar endpoint de verificação de saúde da API.

---

## 12. Requisitos Não Funcionais

### RNF01 — Simplicidade

O backend deve ser simples o suficiente para ser executado localmente durante a apresentação.

### RNF02 — Baixa latência

As respostas do chat devem ser retornadas em tempo aceitável para demonstração em sala.

Meta: até 10 segundos por resposta.

### RNF03 — Rastreabilidade

Toda resposta gerada pelo tutor deve retornar ao menos uma fonte recuperada do Pinecone, quando houver contexto suficiente.

### RNF04 — Configuração externa

Chaves de API, nome do índice Pinecone e modelo de LLM devem ser configurados por variáveis de ambiente.

### RNF05 — Documentação

A API deve ser documentada via Swagger/OpenAPI automaticamente pelo FastAPI.

### RNF06 — Segurança básica

As chaves de API não devem ser versionadas no GitHub.

---

## 13. Regras de Negócio

### RN01 — Resposta baseada no conteúdo da disciplina

O tutor deve priorizar respostas com base nos trechos recuperados do Pinecone.

### RN02 — Não inventar fonte

O backend não deve retornar uma fonte que não tenha sido recuperada do Pinecone.

### RN03 — Resposta insuficiente

Quando os chunks recuperados tiverem baixa similaridade ou não forem suficientes, o tutor deve responder que não encontrou informação suficiente no material.

### RN04 — Diagnóstico simples

O diagnóstico não precisa ser gerado dinamicamente por IA na primeira versão. Pode ser baseado em perguntas previamente cadastradas no backend.

### RN05 — Sem autenticação

O sistema não terá login na versão de demonstração.

---

## 14. Critérios de Aceite

### CA01 — Chat com RAG

Dado que o Pinecone está alimentado com o PDF da disciplina, quando o usuário enviar uma pergunta sobre um conteúdo existente, então o backend deve retornar uma resposta baseada nos chunks recuperados.

### CA02 — Fonte obrigatória

Dado que a pergunta foi respondida com contexto recuperado, quando o backend retornar a resposta, então deve incluir ao menos uma fonte com aula, página ou tema.

### CA03 — Consulta com filtro

Dado que o usuário selecionou um tema, quando a pergunta for enviada, então o backend deve aplicar filtro de metadados no Pinecone sempre que possível.

### CA04 — Busca técnica

Dado um texto de consulta, quando o endpoint `/rag/search` for chamado, então o backend deve retornar os chunks mais similares encontrados no Pinecone.

### CA05 — Diagnóstico

Dado que o usuário concluiu um quiz, quando enviar as respostas, então o backend deve retornar pontuação, lacunas e recomendação.

### CA06 — Plano de estudo

Dado um conjunto de lacunas, quando o frontend solicitar plano de estudo, então o backend deve retornar uma sequência ordenada de tópicos para revisão.

### CA07 — Execução local

Dado que as variáveis de ambiente estão configuradas, quando o backend for iniciado localmente, então a API deve estar disponível e documentada em `/docs`.

---

## 15. Script de Ingestão do PDF

O backend deve conter um script executável para alimentar o Pinecone.

Comando sugerido:

```bash
python -m app.scripts.ingest_pdf_to_pinecone --file data/disciplina_ia.pdf
```

Responsabilidades do script:

```text
1. Ler o PDF.
2. Extrair texto por página.
3. Limpar caracteres desnecessários.
4. Dividir o texto em chunks.
5. Gerar embeddings.
6. Montar metadados.
7. Enviar vetores para o Pinecone.
8. Exibir resumo da ingestão.
```

Saída esperada:

```text
PDF carregado: disciplina_ia.pdf
Páginas processadas: 120
Chunks gerados: 430
Vetores enviados ao Pinecone: 430
Namespace: disciplina-ia
Status: ingestão concluída com sucesso
```

---

## 16. Prompt Base do Tutor

```text
Você é o TutorIA CC0121, um tutor educacional da disciplina de Inteligência Artificial.

Responda à pergunta do aluno usando apenas o contexto fornecido.
Explique de forma clara, objetiva e didática.
Quando útil, use exemplos simples.
Se o contexto não trouxer informação suficiente, informe que o material recuperado não contém dados suficientes para responder com segurança.
Não invente fontes.
Não cite conteúdos que não estejam no contexto.

Contexto recuperado:
{context}

Pergunta do aluno:
{question}

Resposta:
```

---

## 17. Modelo de Dados Interno

### ChatRequest

```python
class ChatRequest(BaseModel):
    question: str
    topic_id: str | None = None
    top_k: int = 5
```

### ChatResponse

```python
class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
    retrieved_chunks: list[str]
    confidence: float | None = None
```

### Source

```python
class Source(BaseModel):
    aula: str | None = None
    titulo_aula: str | None = None
    tema: str | None = None
    topico: str | None = None
    pagina: int | None = None
    score: float | None = None
```

---

## 18. Roadmap de Desenvolvimento

### Etapa 1 — Setup inicial

- Criar projeto FastAPI.
- Configurar `.env`.
- Criar endpoint `/health`.
- Configurar CORS para o Flutter.

### Etapa 2 — Pinecone

- Criar serviço de conexão com Pinecone.
- Criar índice no Pinecone.
- Testar consulta simples.

### Etapa 3 — Ingestão do PDF

- Implementar leitura do PDF.
- Implementar chunking.
- Gerar embeddings.
- Enviar vetores para o Pinecone.

### Etapa 4 — RAG

- Implementar geração de embedding da pergunta.
- Consultar Pinecone.
- Montar prompt com chunks.
- Chamar LLM.
- Retornar resposta com fontes.

### Etapa 5 — Diagnóstico

- Criar perguntas fixas por tema.
- Criar endpoint de quiz.
- Criar correção e identificação de lacunas.

### Etapa 6 — Plano de estudo

- Criar geração de plano por lacunas.
- Integrar com diagnóstico.

### Etapa 7 — Testes e documentação

- Criar README.
- Testar endpoints no Swagger.
- Validar fluxo com Flutter.

---

## 19. Definição de MVP

O MVP do backend estará pronto quando:

- o PDF tiver sido processado e indexado no Pinecone;
- o endpoint `/chat` responder perguntas com base no Pinecone;
- as respostas retornarem fontes;
- o endpoint `/rag/search` permitir testar a recuperação dos chunks;
- o endpoint de diagnóstico funcionar;
- o endpoint de plano de estudo funcionar;
- a API estiver acessível para o app Flutter.

---

## 20. Riscos e Mitigações

| Risco | Impacto | Mitigação |
|---|---|---|
| PDF mal extraído | Respostas ruins | Revisar chunks e limpar texto antes do upsert |
| Chunks muito grandes | Recuperação imprecisa | Usar chunks entre 500 e 1000 tokens |
| Chunks muito pequenos | Falta de contexto | Usar overlap entre chunks |
| Pinecone sem dados | Chat não responde | Criar endpoint ou log para validar total de vetores |
| LLM inventar resposta | Perda de confiança | Prompt restringindo resposta ao contexto |
| Latência alta | Demo prejudicada | Usar top_k pequeno e modelo leve |
| Falha de chave API | Sistema indisponível | Validar env vars no startup |

---

## 21. Considerações Finais

O backend do TutorIA CC0121 será estruturado para demonstrar um fluxo real de RAG aplicado à educação. O Pinecone será usado como banco vetorial principal, alimentado previamente com o PDF da disciplina. A FastAPI atuará como camada de orquestração entre o frontend Flutter, o Pinecone e o modelo de linguagem.

A proposta é adequada para demonstração em sala porque mantém o escopo simples, mas apresenta conceitos técnicos relevantes: ingestão de documentos, embeddings, banco vetorial, recuperação semântica, geração aumentada por contexto, diagnóstico de lacunas e plano de estudo personalizado.
