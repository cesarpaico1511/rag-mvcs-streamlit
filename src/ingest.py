from pathlib import Path
from langchain_chroma import Chroma
from src.config import DOCS_DIR, VECTORSTORE_DIR
from src.loader import load_file, split_docs
from src.embeddings import get_embeddings

def index_documents():
    all_chunks = []
    for file in Path(DOCS_DIR).glob("*"):
        docs = load_file(file)
        chunks = split_docs(docs)
        for c in chunks:
            c.metadata["source_file"] = file.name
        all_chunks.extend(chunks)

    db = Chroma(
        collection_name="mvcs_tramites_servicios",
        embedding_function=get_embeddings(),
        persist_directory=str(VECTORSTORE_DIR)
    )
    db.add_documents(all_chunks)
    return len(all_chunks)

if __name__ == "__main__":
    total = index_documents()
    print(f"Chunks indexados: {total}")
