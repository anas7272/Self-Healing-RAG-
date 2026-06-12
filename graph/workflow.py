from typing import TypedDict

from langgraph.graph import END, StateGraph, START

from utils.retriever import retrieve
from agents.generator import generate
from agents.critic import critic
from agents.rewriter import rewrite
from agents.memory_search import memory_search


class GraphState(TypedDict):
    original_question: str
    question: str
    rewritten_question: str
    memory_hit: bool
    chunks: list
    used_chunks: list
    answer: str
    critic_result: str
    retry_count: int
    workflow_log: list


graph = StateGraph(GraphState)

graph.add_node("memory", memory_search)
graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)
graph.add_node("critic", critic)
graph.add_node("rewrite", rewrite)

graph.add_edge(START, "memory")


def memory_route(state):
    if state["memory_hit"]:
        return END
    return "retrieve"


graph.add_conditional_edges("memory", memory_route)

graph.add_edge("retrieve", "generate")
graph.add_edge("generate", "critic")


def route(state):
    if state["critic_result"] == "PASS":
        return END

    # BUG FIX: retry_count starts at 0, rewriter increments it to 1.
    # Old condition `>= 1` meant: stop after first rewrite attempt.
    # Fixed to `>= 2`: allow up to 2 rewrite+retrieve attempts before giving up.
    if state["retry_count"] >= 2:
        return END

    return "rewrite"


graph.add_conditional_edges("critic", route)
graph.add_edge("rewrite", "retrieve")

workflow = graph.compile()
