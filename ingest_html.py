"""
Ingestão a partir dos HTMLs das aulas — sem artefatos de conversão PDF.
Extrai texto limpo do <div class="container"> de cada Aula_*.html em docs/.
Usa tiktoken para chunking por tokens. Salva em data/chunks.json.
"""
import glob
import json
import os
import re

import tiktoken
from bs4 import BeautifulSoup

DOCS_DIR = "docs"
OUTPUT_PATH = "data/chunks.json"
ENCODING = "cl100k_base"
CHUNK_TOKENS = 800
OVERLAP_TOKENS = 100

# Mapa nome-de-arquivo → (aula_id, titulo)
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


def extrair_texto_html(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Conteúdo principal — ignora header/nav/footer
    container = soup.find("div", class_="container")
    if not container:
        container = soup.find("body")

    # Remove scripts e styles embutidos
    for tag in container.find_all(["script", "style"]):
        tag.decompose()

    # Extrai texto com separadores legíveis
    texto = container.get_text(separator=" ", strip=True)

    # Remove espaços múltiplos e quebras excessivas
    texto = re.sub(r"\s{2,}", " ", texto)
    return texto.strip()


def chunkar(texto: str, enc: tiktoken.Encoding) -> list[str]:
    tokens = enc.encode(texto)
    stride = CHUNK_TOKENS - OVERLAP_TOKENS
    chunks = []
    i = 0
    while i < len(tokens):
        trecho_tokens = tokens[i : i + CHUNK_TOKENS]
        chunks.append(enc.decode(trecho_tokens))
        i += stride
    return chunks


def main():
    enc = tiktoken.get_encoding(ENCODING)
    paths = sorted(glob.glob(os.path.join(DOCS_DIR, "Aula_*.html")))

    if not paths:
        print(f"Nenhum arquivo Aula_*.html encontrado em {DOCS_DIR}/")
        return

    print(f"Arquivos encontrados: {len(paths)}")
    todos_chunks = []

    for path in paths:
        aula_id, titulo = _aula_meta(path)
        texto = extrair_texto_html(path)
        trechos = chunkar(texto, enc)
        filename = os.path.basename(path)

        for idx, trecho in enumerate(trechos):
            todos_chunks.append({
                "id": f"{aula_id}_chunk{idx:03d}",
                "text": trecho,
                "aula": aula_id,
                "titulo_aula": titulo,
                "chunk_index": idx,
                "source": filename,
                "tokens": len(enc.encode(trecho)),
            })

        print(f"  {filename[:45]}: {len(trechos)} chunks")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(todos_chunks, f, ensure_ascii=False, indent=2)

    total_tokens = sum(c["tokens"] for c in todos_chunks)
    print(f"\n✓ {len(todos_chunks)} chunks salvos em {OUTPUT_PATH}")
    print(f"  Total de tokens: {total_tokens}")
    print(f"  Aulas indexadas: {sorted(set(c['aula'] for c in todos_chunks))}")


if __name__ == "__main__":
    main()
