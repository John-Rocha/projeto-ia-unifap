"""
Script de ingestão local — sem OpenAI, sem Pinecone.
Usa tiktoken para chunking por tokens.
Salva chunks em data/chunks.json.
"""
import json
import os
import time
import tiktoken
from pypdf import PdfReader

PDF_PATH = "data/disciplina_ia.pdf"
OUTPUT_PATH = "data/chunks.json"
ENCODING = "cl100k_base"
CHUNK_TOKENS = 800
OVERLAP_TOKENS = 100
BATCH_LOG = 20


def extrair_paginas(path: str) -> list[dict]:
    reader = PdfReader(path)
    paginas = []
    for i, page in enumerate(reader.pages):
        texto = page.extract_text() or ""
        texto = " ".join(texto.split())
        if texto.strip():
            paginas.append({"pagina": i + 1, "texto": texto})
    return paginas


def chunkar_com_tiktoken(texto: str, pagina: int, enc: tiktoken.Encoding) -> list[dict]:
    tokens = enc.encode(texto)
    chunks = []
    i = 0
    idx = 0
    stride = CHUNK_TOKENS - OVERLAP_TOKENS
    while i < len(tokens):
        token_slice = tokens[i : i + CHUNK_TOKENS]
        trecho = enc.decode(token_slice)
        chunks.append({
            "id": f"pag{pagina:03d}_chunk{idx:03d}",
            "text": trecho,
            "pagina": pagina,
            "chunk_index": idx,
            "source": os.path.basename(PDF_PATH),
            "tokens": len(token_slice),
        })
        i += stride
        idx += 1
    return chunks


def main():
    enc = tiktoken.get_encoding(ENCODING)
    print(f"Encoder: {ENCODING}")
    print(f"PDF: {PDF_PATH}")

    paginas = extrair_paginas(PDF_PATH)
    print(f"Páginas com texto: {len(paginas)}")

    todos_chunks = []
    for p in paginas:
        todos_chunks.extend(chunkar_com_tiktoken(p["texto"], p["pagina"], enc))

    print(f"Chunks gerados: {len(todos_chunks)}")

    # Mostrar como o modelo fatiou o texto do primeiro chunk (igual ao exemplo do tiktoken)
    if todos_chunks:
        amostra = todos_chunks[0]
        tokens_amostra = enc.encode(amostra["text"][:200])
        print("\nComo o modelo fatia o início do primeiro chunk:")
        for t in tokens_amostra[:10]:
            print(f"  {t} → '{enc.decode([t])}'")
        print(f"  ... ({len(tokens_amostra)} tokens no trecho)")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(todos_chunks, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Chunks salvos em {OUTPUT_PATH}")
    print(f"  Total de chunks: {len(todos_chunks)}")
    total_tokens = sum(c["tokens"] for c in todos_chunks)
    print(f"  Total de tokens: {total_tokens}")


if __name__ == "__main__":
    main()
