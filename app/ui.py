import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")

st.set_page_config(page_title="Agentic RAG", layout="wide")

st.title("Agentic RAG System")

tab1, tab2 = st.tabs(["Ingest Document", "Chat"])

# ---------------------------
# Document Ingestion
# ---------------------------

with tab1:
    st.header("Ingest Text Document")

    text = st.text_area("Paste document text", height=300)

    if st.button("Ingest"):
        if text.strip() == "":
            st.warning("Please enter some text")
        else:
            response = requests.post(
                f"{BACKEND_URL}/ingest/text",
                json={"text": text}
            )

            if response.status_code == 200:
                data = response.json()
                st.success(f"Queued {data['chunks']} chunks")
            else:
                st.error("Failed to ingest document")


# ---------------------------
# Chat Interface
# ---------------------------

with tab2:
    st.header("Chat with your knowledge base")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.chat_input("Ask a question")

    if question:

        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.write(question)

        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={"question": question}
        )

        answer = response.json()["answer"]

        with st.chat_message("assistant"):
            st.write(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )