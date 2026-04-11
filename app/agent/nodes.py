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


def grade_node(state):
    question = state["question"]
    context = state["context"]

    prompt = f"""
        You are a strict evaluator.

        Check if the retrieved context is relevant to the question.

        Rules:
        - If the context clearly contains information to answer the question → say YES
        - Otherwise → say NO
        - Only respond with YES or NO

        Question:
        {question}

        Context:
        {context}
        """

    response = llm.invoke(prompt).content.strip().upper()

    return {
        "is_relevant": "YES" in response
    }

def rewrite_node(state):
    question = state["question"]

    prompt = f"""
        You are an expert query rewriter.

        Rewrite the user question to make it more specific and searchable.

        Rules:
        - Keep the meaning same
        - Make it clearer and more detailed
        - Do NOT answer the question
        - Only return the rewritten question

        Original question:
        {question}
        """

    response = llm.invoke(prompt).content.strip()

    return {
        "question": response,
        "retries": state["retries"] + 1
    }