import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import document_loader, vector_store, rag_answer, reset_chat
from langchain_text_splitters import RecursiveCharacterTextSplitter
import streamlit as st


st.title("📄 Documentation RAG Assistant")
st.write("Load a text-file documentation link and ask grounded questions.")


# ---------------------------
# URL INPUT + DOCUMENT LOAD
# ---------------------------

url = st.text_input("Enter Document URL (.txt only)")

if st.button("Load Document"):
    if not url:
        st.error("Please enter a valid URL.")
    else:
        st.write("⏳ Loading document...")
        text = document_loader.load(url)

        if not text:
            st.error("❌ Failed to load document.")
        else:
            st.success("Document loaded successfully!")

            reset_chat()  # NEW: Clear chat history

            splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
            chunks = splitter.split_text(text)

            vector_store.add_texts(chunks)
            st.success(f"Indexed {len(chunks)} chunks!")

            st.session_state["doc_loaded"] = True
else:
    st.session_state["doc_loaded"] = st.session_state.get("doc_loaded", False)


# --------------------------------
# CHAT INTERFACE (AFTER DOCUMENT)
# --------------------------------

if st.session_state["doc_loaded"]:

    st.subheader("💬 Chat with Document")

    # Display previous messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Chat input
    user_query = st.chat_input("Ask a question about the document...")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        st.chat_message("user").write(user_query)

        answer = rag_answer(user_query)

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.chat_message("assistant").write(answer)
