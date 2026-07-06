"""
Ingestão: HTML das aulas → OpenAI embeddings → Pinecone.
Usa os mesmos HTMLs de docs/ (sem artefatos de PDF) e gera vetores semânticos.
Execute uma vez após alterar o material ou criar o índice no Pinecone.
"""
import glob
import os
import re
import time

import tiktoken
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

load_dotenv()

DOCS_DIR            = "docs"
ENCODING            = "cl100k_base"
CHUNK_TOKENS        = 800
OVERLAP_TOKENS      = 100
BATCH_SIZE          = 50
EMBEDDING_MODEL     = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", 512))
NAMESPACE           = os.getenv("PINECONE_NAMESPACE", "disciplina-ia")

oai   = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc    = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(host=os.getenv("PINECONE_HOST"))

_AULA_MAP = {
    "Aula_01": ("aula01", "Panorama da IA"),
    "Aula_02": ("aula02", "Agentes Inteligentes"),
    "Aula_03": ("aula03", "Busca e Otimização"),
    "Aula_04": ("aula04", "Busca Local e Adversarial"),
    "Aula_05": ("aula05", "Representação do Conhecimento"),
    "Aula_06": ("aula06", "ML Supervisionado"),
    "Aula_07": ("aula07", "Clustering e Ensembles"),
    "Aula_08": ("aula08", "Tópicos Modernos: LLMs, RAG e Agentes"),
}


def _aula_meta(filename: str) -> tuple[str, str]:
    base = os.path.basename(filename)
    for prefix, (aula_id, titulo) in _AULA_MAP.items():
        if base.startswith(prefix):
            return aula_id, titulo
    return "desconhecida", base


def extrair_texto(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    container = soup.find("div", class_="container") or soup.find("body")
    for tag in container.find_all(["script", "style"]):
        tag.decompose()
    texto = container.get_text(separator=" ", strip=True)
    return re.sub(r"\s{2,}", " ", texto).strip()


def chunkar(texto: str, enc: tiktoken.Encoding) -> list[str]:
    tokens = enc.encode(texto)
    stride  = CHUNK_TOKENS - OVERLAP_TOKENS
    chunks  = []
    i = 0
    while i < len(tokens):
        chunks.append(enc.decode(tokens[i : i + CHUNK_TOKENS]))
        i += stride
    return chunks


def embed(texto: str) -> list[float]:
    resp = oai.embeddings.create(
        input=texto,
        model=EMBEDDING_MODEL,
        dimensions=EMBEDDING_DIMENSION,
    )
    return resp.data[0].embedding


def upsert_batch(vetores: list[dict]):
    for i in range(0, len(vetores), BATCH_SIZE):
        batch = vetores[i : i + BATCH_SIZE]
        index.upsert(vectors=batch, namespace=NAMESPACE)
        print(f"  upsert {i + len(batch)}/{len(vetores)}")
        time.sleep(0.3)


def main():
    enc   = tiktoken.get_encoding(ENCODING)
    paths = sorted(glob.glob(os.path.join(DOCS_DIR, "Aula_*.html")))

    if not paths:
        print(f"Nenhum arquivo Aula_*.html encontrado em {DOCS_DIR}/")
        return

    print(f"Arquivos: {len(paths)}")
    vetores: list[dict] = []

    for path in paths:
        aula_id, titulo = _aula_meta(path)
        texto   = extrair_texto(path)
        trechos = chunkar(texto, enc)
        filename = os.path.basename(path)
        print(f"  {filename[:45]}: {len(trechos)} chunks")

        for idx, trecho in enumerate(trechos):
            vec_id = f"{aula_id}_chunk{idx:03d}"
            vetor  = embed(trecho)
            vetores.append({
                "id":     vec_id,
                "values": vetor,
                "metadata": {
                    "text":        trecho,
                    "aula":        aula_id,
                    "titulo_aula": titulo,
                    "chunk_index": idx,
                    "source":      filename,
                },
            })
            time.sleep(0.05)

    print(f"\nTotal: {len(vetores)} vetores. Enviando ao Pinecone...")
    upsert_batch(vetores)

    stats    = index.describe_index_stats()
    ns_count = stats.namespaces.get(NAMESPACE, {})
    print(f"\n Ingestão concluída — namespace '{NAMESPACE}': {ns_count}")


if __name__ == "__main__":
    main()
