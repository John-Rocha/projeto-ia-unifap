import os
import time
from pypdf import PdfReader
from openai import OpenAI
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

# Clientes
oai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc  = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(host=os.getenv("PINECONE_HOST"))

NAMESPACE           = os.getenv("PINECONE_NAMESPACE", "disciplina-ia")
EMBEDDING_MODEL     = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", 512))
CHUNK_SIZE          = int(os.getenv("CHUNK_SIZE", 800))
CHUNK_OVERLAP       = int(os.getenv("CHUNK_OVERLAP", 100))
PDF_PATH         = "data/disciplina_ia.pdf"
BATCH_SIZE       = 50  # vetores por upsert


def extrair_paginas(path: str) -> list[dict]:
    reader = PdfReader(path)
    paginas = []
    for i, page in enumerate(reader.pages):
        texto = page.extract_text() or ""
        texto = " ".join(texto.split())  # remove whitespace excessivo
        if texto.strip():
            paginas.append({"pagina": i + 1, "texto": texto})
    return paginas


def chunkar(texto: str, pagina: int) -> list[dict]:
    words = texto.split()
    chunks = []
    i = 0
    idx = 0
    while i < len(words):
        trecho = " ".join(words[i : i + CHUNK_SIZE])
        chunks.append({"texto": trecho, "pagina": pagina, "chunk_index": idx})
        i += CHUNK_SIZE - CHUNK_OVERLAP
        idx += 1
    return chunks


def gerar_embedding(texto: str) -> list[float]:
    resp = oai.embeddings.create(input=texto, model=EMBEDDING_MODEL, dimensions=EMBEDDING_DIMENSION)
    return resp.data[0].embedding


def montar_vetor(chunk: dict, embedding: list[float]) -> dict:
    vec_id = f"pag{chunk['pagina']:03d}_chunk{chunk['chunk_index']:03d}"
    return {
        "id": vec_id,
        "values": embedding,
        "metadata": {
            "text":        chunk["texto"],
            "pagina":      chunk["pagina"],
            "chunk_index": chunk["chunk_index"],
            "source":      os.path.basename(PDF_PATH),
        },
    }


def upsert_em_batches(vetores: list[dict]):
    for i in range(0, len(vetores), BATCH_SIZE):
        batch = vetores[i : i + BATCH_SIZE]
        index.upsert(vectors=batch, namespace=NAMESPACE)
        print(f"  upsert {i + len(batch)}/{len(vetores)}")
        time.sleep(0.5)  # evita rate limit


def main():
    print(f"PDF: {PDF_PATH}")
    paginas = extrair_paginas(PDF_PATH)
    print(f"Páginas com texto: {len(paginas)}")

    todos_chunks = []
    for p in paginas:
        todos_chunks.extend(chunkar(p["texto"], p["pagina"]))
    print(f"Chunks gerados: {len(todos_chunks)}")

    print("Gerando embeddings...")
    vetores = []
    for i, chunk in enumerate(todos_chunks):
        emb = gerar_embedding(chunk["texto"])
        vetores.append(montar_vetor(chunk, emb))
        if (i + 1) % 10 == 0:
            print(f"  {i + 1}/{len(todos_chunks)} embeddings")
        time.sleep(0.05)  # evita rate limit OpenAI

    print(f"Enviando {len(vetores)} vetores ao Pinecone...")
    upsert_em_batches(vetores)

    stats = index.describe_index_stats()
    ns_count = stats.namespaces.get(NAMESPACE, {})
    print("\n--- Ingestão concluída ---")
    print(f"Namespace:       {NAMESPACE}")
    print(f"Vetores no index: {ns_count}")


if __name__ == "__main__":
    main()