import streamlit as st
from ingest import chat_model, ingest_url, build_prompt


if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_url" not in st.session_state:
    st.session_state.current_url = None

st.title("RAG chatbot - chat with any webpage")

url = st.text_input("Enter a URL to chat about")

if st.button("Ingest URL"):
    if url:
        with st.spinner("Scraping, chunking and embedding..."):
            st.session_state.retriever = ingest_url(url)
            st.session_state.current_url = url
            st.session_state.chat_history = []  # reset memory for the new document
        st.success(f"Ready! You can now ask questions about: {url}")
    else:
        st.warning("Please enter a URL first.")

if st.session_state.retriever:
    for q, a in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(q)
        with st.chat_message("assistant"):
            st.write(a)

    question = st.chat_input("Ask a question about the page")
    if question:
        with st.chat_message("user"):
            st.write(question)

        retrieved_docs = st.session_state.retriever.invoke(question)
        prompt = build_prompt(question, retrieved_docs, st.session_state.chat_history)
        response = chat_model.invoke(prompt)
        answer = response.content

        with st.chat_message("assistant"):
            st.write(answer)

        st.session_state.chat_history.append((question, answer))