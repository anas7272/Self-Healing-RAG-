import streamlit as st

from graph.workflow import workflow

st.set_page_config(
    page_title="Self-Healing RAG",
    layout="wide"
)

st.title(" Self-Healing RAG")

question = st.text_input(
    "Ask about company"
)

if st.button("Ask"):

    trace_placeholder = st.empty()

    logs = []

    final_state = {
        "original_question": question,
        "question": question,
        "rewritten_question": "",
        "memory_hit": False,
        "chunks": [],
        "used_chunks": [],
        "answer": "",
        "critic_result": "",
        "retry_count": 0,
        "workflow_log": []
    }

    icons = {
        "memory": "  Memory Search",
        "retrieve": " Retriever",
        "generate": " Generator",
        "critic": " Critic",
        "rewrite": " Rewriter"
    }

    for event in workflow.stream(
        {
            "original_question": question,
            "memory_hit": False,
            "question": question,
            "rewritten_question": "",
            "chunks": [],
            "used_chunks": [],
            "answer": "",
            "critic_result": "",
            "retry_count": 0,
            "workflow_log": []
        }
    ):

        print("\nEVENT:")
        print(event)

        node = list(event.keys())[0]

        logs.append(
            icons.get(node, node)
        )

        trace_placeholder.markdown(
            "## 🔄 Live Workflow\n\n"
            + " -> ".join(logs)
        )

        node_state = list(event.values())[0]

        final_state.update(node_state)

    st.markdown("---")
    if final_state:

        state = final_state

        st.markdown("---")

        st.subheader("📝 Query Journey")

        st.info(
            f"Original Query: {state.get('original_question', '')}"
        )

        if state.get("rewritten_question", ""):

            st.success(
                f"Optimized Query: {state.get('rewritten_question', '')}"
            )

        st.markdown("---")

        st.subheader("💬 Final Answer")

        st.success(
            state.get("answer", "")
        )
        st.subheader("Chunks Used for Answer Generation :")

        for i, chunk in enumerate(
            state.get("used_chunks", []),
            start=1
        ):
            with st.expander(f"Chunk {i}"):

                st.write(chunk)