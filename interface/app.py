import sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

import streamlit as st
from main import load_document, rag_answer, chat_history


st.title("📘 Documentation RAG Assistant")

url = st.text_input("Paste a .txt documentation URL (SvelteKit llms.txt)")

if st.button("Load Document"):
    text, msg = load_document(url)
    if text:
        st.success(msg)
        st.text_area("Document Preview", text[:2000], height=200)
    else:
        st.error(msg)

query = st.text_input("Ask a question:")

if st.button("Ask"):
    answer = rag_answer(query)
    st.write("### 📌 Answer:")
    st.write(answer)
