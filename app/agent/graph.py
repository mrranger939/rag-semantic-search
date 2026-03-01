from langgraph.graph import StateGraph
from app.agent.state import AgentState
from app.agent.nodes import retrieve_node, generate_node

builder = StateGraph(AgentState)

builder.add_node("retrieve", retrieve_node)
builder.add_node("generate", generate_node)

builder.set_entry_point("retrieve")
builder.add_edge("retrieve", "generate")
builder.set_finish_point("generate")

graph = builder.compile()