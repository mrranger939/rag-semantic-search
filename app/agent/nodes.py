from app.search import search_query
from app.agent.state import AgentState
from app.agent.llm import llm

def retrieve_node(state: AgentState):
    context = search_query(state['question'], limit=3)
    return {
        "context": context
    }

def generate_node(state: AgentState):
    prompt = f"""
    Answer the question using ONLY the context below.
    
    context: 
    {state['context']}

    Question:
    {state['question']}

    Give clear and concise answer.
    """

    response = llm.invoke(prompt)
    return {
        "answer": response.content
    }