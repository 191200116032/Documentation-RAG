import os
from dotenv import load_dotenv
load_dotenv()

from infrastructure.web_loader import WebDocumentLoader
from infrastructure.groq_adapter import GroqLLMProvider
from infrastructure.chroma_adapter import ChromaVectorStore
from infrastructure.hf_embedding_adapter import HFEmbeddingProvider

# ----------------------
# INITIALIZE COMPONENTS
# ----------------------

# LLM
llm = GroqLLMProvider(model="llama-3.3-70b-versatile")

# Embeddings (HF MiniLM - free)
embedding_provider = HFEmbeddingProvider()
embed_fn = embedding_provider.embed

# Vector DB
vector_store = ChromaVectorStore(
    collection_name="documentation_chunks_v6",
    embedding_fn=embed_fn
)

# Loader
document_loader = WebDocumentLoader()

# ----------------------
# CHAT HISTORY
# ----------------------
chat_history = []

def reset_chat():
    global chat_history
    chat_history = []

# ----------------------
# RAG ANSWER FUNCTION
# ----------------------
def rag_answer(query):
    global chat_history

    # Retrieve relevant docs
    retrieved_docs = vector_store.similarity_search(query, k=3)
    context = "\n\n".join(retrieved_docs) if retrieved_docs else ""

    # Build chat history
    history = ""
    for turn in chat_history:
        history += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n\n"

    prompt = f"""
You are a RAG assistant. Use ONLY the provided document.

DOCUMENT CONTEXT:
{context}

CHAT HISTORY:
{history}

QUESTION: {query}

If the answer is not present in the context, reply: "Not found in document."
"""

    answer = llm.generate(prompt)

    # Save history
    chat_history.append({"user": query, "assistant": answer})

    return answer
