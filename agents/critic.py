from langchain_core.documents import Document
from agents.memory_search import memory_db
from agents.llm import get_llm

llm = get_llm()


def save_to_memory(state):
    results = memory_db.similarity_search_with_score(
        state["question"],
        k=1
    )

    if results:
        doc, score = results[0]

        # BUG FIX: Old threshold was 0.05 — almost nothing ever got saved to memory.
        # Fixed to 0.15: skip saving only if a near-identical Q&A already exists.
        if score < 0.15:
            return

    state["workflow_log"].append("🧠 Learning New Knowledge")

    memory_db.add_documents(
        [
            Document(
                page_content=state["question"],
                metadata={"answer": state["answer"]}
            )
        ]
    )

    state["workflow_log"].append("💾 Memory Saved")


def critic(state):
    answer = state["answer"].lower()

    context = " ".join(
        [doc.page_content for doc in state["chunks"]]
    ).lower()

    overlap = sum(
        1 for word in answer.split()
        if len(word) > 4 and word in context
    )

    # Fast fail — answer explicitly admits no info found
    if (
        "information not found" in answer
        or "does not provide information" in answer
        or "does not provide the name" in answer
        or "context does not" in answer
        or "no information" in answer
    ):
        state["critic_result"] = "FAIL"
        state["workflow_log"].append("❌ Critic FAIL (No Answer Found)")
        return state

    # Fast pass — answer words overlap well with context
    if overlap >= 2:
        state["critic_result"] = "PASS"
        state["workflow_log"].append("✅ Critic PASS (Fast Check)")
        save_to_memory(state)
        return state

    # Hard cases go to LLM
    state["workflow_log"].append("LLM Critic Activates")

    prompt = f"""
Question:
{state["question"]}

Answer:
{state["answer"]}

Context:
{context}

Check:
1. Is answer grounded in context?
2. Any hallucination?
3. Is answer relevant?

Reply ONLY:
PASS
or
FAIL
"""

    result = llm.invoke(prompt)
    state["critic_result"] = result.content.strip().upper()

    if state["critic_result"] == "PASS":
        state["workflow_log"].append("✅ Critic PASS (LLM)")
        save_to_memory(state)
    else:
        state["workflow_log"].append("❌ Critic FAIL (LLM)")

    return state
