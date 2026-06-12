import streamlit as st
from langchain_chroma import Chroma
from utils.embeddings import get_embeddings


@st.cache_resource
def get_memory_db():
    return Chroma(
        collection_name="query_memory",
        persist_directory="memory_store",
        embedding_function=get_embeddings()
    )


memory_db = get_memory_db()


def memory_search(state):
    docs = memory_db.similarity_search_with_score(
        state["question"],
        k=1
    )

    if docs:
        doc, score = docs[0]

        print("Memory Score:", score)

        # BUG FIX: Old threshold was 0.03 — almost never triggered.
        # Chroma cosine distance: 0.0 = identical, ~1.0 = unrelated.
        # A score < 0.15 means very high similarity — safe to use cached answer.
        if score < 0.15:
            state["answer"] = doc.metadata["answer"]
            state["memory_hit"] = True
            state["workflow_log"].append("🧠 Memory Hit")
            return state

    state["memory_hit"] = False
    state["workflow_log"].append("🧠 Memory Miss")
    return state
