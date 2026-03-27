import streamlit as st
import requests

st.title("🤖 AI Chatbot (Gemini + RAG + Agent)")

query = st.text_input("Ask something:")

if st.button("Send"):
    response = requests.get(
        "http://localhost:8000/chat",
        params={"query": query},
        stream=True
    )

    output = ""
    placeholder = st.empty()

    for chunk in response.iter_content(chunk_size=10):
        if chunk:
            output += chunk.decode()
            placeholder.write(output)