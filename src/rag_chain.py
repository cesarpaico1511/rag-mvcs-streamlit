from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import GEMINI_MODEL
from src.prompts import SYSTEM_PROMPT
from src.retriever import retrieve

def ask_rag(question):
    docs = retrieve(question)
    if not docs:
        return {"answer": "No tengo evidencia suficiente en las fuentes cargadas", "sources": []}

    context = "\n\n".join([d.page_content for d, s in docs])
    sources = [{"file": d.metadata.get("source_file"), "score": s} for d, s in docs]

    llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, temperature=0.1)
    prompt = f"{SYSTEM_PROMPT}\n\nContexto:\n{context}\n\nPregunta:\n{question}"
    answer = llm.invoke(prompt).content

    return {"answer": answer, "sources": sources}
