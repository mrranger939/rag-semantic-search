from app.search import search_query
from app.agent.state import AgentState
from app.agent.llm import llm

def retrieve_node(state: AgentState):
    context = search_query(state['question'], limit=7)
    return {
        "context": context
    }

def generate_node(state: AgentState):
    prompt = f"""
        You are a helpful assistant answering questions using the provided documents.

        Rules:
        1. Use ONLY the provided context.
        2. Do NOT copy the context verbatim.
        3. Summarize the information clearly.
        4. Always cite the document name like this: (Source: document_name).
        5. If the answer is not present in the context, say:
        "I don't have enough information."

        Context:
        {state['context']}

        Question:
        {state['question']}

        Answer:
        """

    response = llm.invoke(prompt)
    return {
        "answer": response.content
    }