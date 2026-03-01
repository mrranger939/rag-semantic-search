from app.agent.graph import graph

while True:
    query = input("\nAsk something (type 'end' to exit): ")

    if not query.strip():
        print("Please enter a valid question.")
        continue

    if query.lower() == "end":
        print("Exiting...")
        break

    result = graph.invoke({
        "question": query,
        "context": "",
        "answer": ""
    })

    print("\nFinal Answer:\n")
    print(result["answer"])