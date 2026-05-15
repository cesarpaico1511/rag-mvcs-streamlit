import streamlit as st
from src.rag_chain import ask_rag

st.set_page_config(page_title="Asistente RAG MVCS", page_icon="🏛️", layout="wide")

st.title("🏛️ Asistente RAG MVCS")
st.caption("Consulta documentos oficiales cargados sobre trámites y servicios del MVCS.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("sources"):
            with st.expander("Fuentes utilizadas"):
                st.json(msg["sources"])

question = st.chat_input("Escribe tu pregunta sobre trámites o servicios del MVCS...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Buscando evidencia en documentos cargados..."):
            result = ask_rag(question)

        st.write(result["answer"])

        if result.get("sources"):
            with st.expander("Fuentes utilizadas"):
                st.json(result["sources"])

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sources": result.get("sources", [])
    })
