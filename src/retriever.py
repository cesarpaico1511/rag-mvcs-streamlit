from langchain_chroma import Chroma
from src.config import VECTORSTORE_DIR
from src.embeddings import get_embeddings

def get_vectorstore():
    return Chroma(
        collection_name="mvcs_tramites_servicios",
        embedding_function=get_embeddings(),
        persist_directory=str(VECTORSTORE_DIR)
    )

def retrieve(question, k=4):
    db = get_vectorstore()
    return db.similarity_search_with_relevance_scores(question, k=k)
