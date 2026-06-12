import streamlit as st
from langchain_chroma import Chroma
from utils.embeddings import get_embeddings


@st.cache_resource
def get_vector_db():
    with st.spinner("Loading Knowledge Base..."):
        return Chroma(
            persist_directory="vectorstore",
            embedding_function=get_embeddings()
        )


def retrieve(state):
    # BUG FIX: db was created at module level before Streamlit context existed.
    # Now we call get_vector_db() inside the function — safe and cached.
    db = get_vector_db()

    retriever = db.as_retriever(
        search_kwargs={"k": 3}
    )

    chunks = retriever.invoke(state["question"])

    state["chunks"] = chunks

    state["workflow_log"].append("🔍 Retriever")

    return state
