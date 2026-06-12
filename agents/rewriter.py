from agents.llm import get_llm
llm = get_llm()

def rewrite(state):

    prompt = f"""
You are an expert Query Understanding and Retrieval Optimization Agent.

Your job is to transform human questions into precise retrieval-friendly queries.

Guidelines:

1. Understand the user's intent, not just the words.
2. Expand abbreviations, slang, informal language, and ambiguous terms.
3. Replace colloquial words with the most likely business/domain terminology.
4. Preserve the original meaning.
5. Do NOT answer the question.
6. Do NOT add information not implied by the query.
7. Generate a query that maximizes retrieval quality from a company knowledge base.
8. Return ONLY the rewritten query.

Examples:

User: boss of company
Rewritten: Who is the CEO of the company?

User: who runs the company
Rewritten: Who is the CEO of the company?

User: company head
Rewritten: Who is the head executive of the company?

User: tech lead
Rewritten: Who is responsible for leading the engineering organization?

User: benefits for workers
Rewritten: What employee benefits does the company provide?

User: leave policy
Rewritten: What is the company's leave and vacation policy?

User: joining process
Rewritten: What is the employee onboarding process?

User: salary cycle
Rewritten: When and how are employees paid?

User: training stuff
Rewritten: What employee training and learning programs are available?

User: insurance
Rewritten: What insurance benefits does the company provide?

Now rewrite this query:

{state["question"]}

Return ONLY the rewritten query.
"""

    result = llm.invoke(prompt)

    state["rewritten_question"] = result.content
    state["question"] = result.content
    state["workflow_log"].append("🔄 Rewriter")

    state["retry_count"] += 1

    return state