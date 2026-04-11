from langgraph.graph import StateGraph
from app.agent.state import AgentState
from app.agent.nodes import retrieve_node, generate_node, grade_node, rewrite_node
from dotenv import load_dotenv
import os

load_dotenv()

MAX_QUERY_RETRIES = int(os.getenv("MAX_QUERY_RETRIES"))


def should_generate(state: AgentState):
    if state['is_relevant']:
        return "generate"
    elif state['retries'] >= MAX_QUERY_RETRIES:
        return "generate"
    else:
        return 'rewrite'

builder = StateGraph(AgentState)

builder.add_node("retrieve", retrieve_node)
builder.add_node("generate", generate_node)
builder.add_node("grade", grade_node)
builder.add_node("rewrite", rewrite_node)

builder.set_entry_point("retrieve")
builder.add_edge('retrieve', 'grade')
builder.add_conditional_edges(
    'grade',
    should_generate,
    {
        "generate": "generate",
        "rewrite": "rewrite"
    }
)
builder.add_edge("rewrite", "retrieve")
builder.set_finish_point("generate")

graph = builder.compile()