import os

from agents.llm import get_llm

llm = get_llm()

def generate(state):

    context = "\n\n".join(
        [doc.page_content for doc in state["chunks"]]
    )

    prompt = f"""
You are a company knowledge assistant.

Answer the question ONLY from the provided context.

Rules:
1. If the answer exists in the context, answer directly.
2. Do not say "Information not found" if relevant information is present.
3. Do not make up information.
4. Be concise.

Question:
{state["question"]}

Context:
{context}

Answer:
"""

    response = llm.invoke(prompt)

    state["answer"] = response.content

    state["used_chunks"] = [
        doc.page_content[:300]
        for doc in state["chunks"]
    ]

    state["workflow_log"].append("Generator")

    return state