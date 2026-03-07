from app.agent.graph import graph

def chat(question: str):
    state = {
        "question": question,
        "context": "",
        "answer": ""
    }

    result = graph.invoke(state)

    return {
        "answer": result["answer"]
    }