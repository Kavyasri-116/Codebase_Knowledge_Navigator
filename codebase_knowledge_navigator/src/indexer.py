from pathlib import Path
import shutil
import tempfile
import chromadb
from langchain_ollama import OllamaEmbeddings

SUPPORTED = {".py", ".js", ".ts", ".java", ".c", ".cpp", ".h", ".hpp", ".html", ".css", ".sql", ".json", ".md", ".txt"}

def _chunks(text: str, chunk_size=1200, overlap=200):
    text = text.replace("\r\n", "\n")
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap
    return chunks

def build_index(source_dir: Path, embedding_model: str) -> str:
    index_dir = Path(tempfile.mkdtemp(prefix="codebase_nav_"))
    source_copy = index_dir / "source_files"
    shutil.copytree(source_dir, source_copy)

    client = chromadb.PersistentClient(path=str(index_dir / "chroma"))
    collection = client.get_or_create_collection("codebase")
    embeddings = OllamaEmbeddings(model=embedding_model)

    ids, docs, metas, vectors = [], [], [], []
    counter = 0
    for path in source_copy.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for n, chunk in enumerate(_chunks(text)):
            if not chunk.strip():
                continue
            ids.append(f"chunk-{counter}")
            docs.append(chunk)
            metas.append({"file": str(path.relative_to(source_copy)), "chunk": n})
            counter += 1
            vectors.append(None)

    if not docs:
        raise ValueError("No supported source files were found.")

    # OllamaEmbeddings embeds one document at a time here for compatibility.
    embedded = embeddings.embed_documents(docs)
    collection.add(ids=ids, documents=docs, metadatas=metas, embeddings=embedded)
    return str(index_dir)
