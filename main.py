import requests
import re
from dotenv import load_dotenv
load_dotenv()

from infrastructure.groq_adapter import GroqLLMProvider
from infrastructure.chroma_adapter import ChromaVectorStore

# GLOBAL STATE
vector_store = None
chat_history = []
current_document_url = None


# ---------------- CHUNKER (Improved) ----------------
def chunk_text(text, chunk_size=800, overlap=150):
    parts = re.split(r'\n\s*\n', text)
    chunks = []
    current = ""

    for part in parts:
        part = part.strip()
        if not part:
            continue

        if len(part) > chunk_size:
            sentences = re.split(r'(?<=[.!?]) +', part)
            for sent in sentences:
                if len(current) + len(sent) < chunk_size:
                    current += sent + " "
                else:
                    chunks.append(current.strip())
                    current = sent + " "
        else:
            if len(current) + len(part) < chunk_size:
                current += part + " "
            else:
                chunks.append(current.strip())
                current = part + " "

    if current:
        chunks.append(current.strip())

    return chunks


# ---------------- LOAD DOCUMENT (now error-safe) ----------------
def load_document(url):
    global vector_store, chat_history, current_document_url

    # Reset if new URL comes
    if url != current_document_url:
        chat_history.clear()
        vector_store = None
        current_document_url = url

    # Validate extension
    if not url.endswith(".txt"):
        return None, "❌ This system only works with .txt documentation files.\n\nPlease scroll to bottom of Svelte docs and copy the *llms.txt* link."

    # Fetch
    try:
        response = requests.get(url, timeout=10)
    except:
        return None, "❌ Failed to reach the URL. Please check your internet or link."

    if response.status_code != 200:
        return None, f"❌ Document returned HTTP {response.status_code}. Please check the link."

    text = response.text.strip()

    if len(text) < 10:
        return None, "❌ The document is empty or invalid."

    # Chunk + embed
    chunks = chunk_text(text)
    vector_store = ChromaVectorStore()
    vector_store.add_texts(chunks)

    return text, "✅ Document loaded and processed successfully."
def rag_answer(query):
    print("🔥 USING NEW RAG FUNCTION")

    global vector_store

    if vector_store is None:
        return "❌ Please load a document first."

    retrieved = []

    # 1) Semantic search
    results = vector_store.search(query, k=5)
    if results:
        retrieved = results

    # 2) Keyword fallback
    if not retrieved:
        keywords = [w.lower() for w in query.split() if len(w) > 3]
        keyword_hits = []
        for chunk in vector_store.raw_chunks:
            if any(k in chunk.lower() for k in keywords):
                keyword_hits.append(chunk)
        if keyword_hits:
            retrieved = keyword_hits[:5]

    # 3) Special handle() handling for hooks docs
    if "handle" in query.lower():
        handle_hits = [c for c in vector_store.raw_chunks if "handle" in c.lower()]
        if handle_hits:
            retrieved = handle_hits[:5]

    # 4) OUT OF SCOPE RESPONSE
    if not retrieved:
        # Extract topics
        topics = []
        for chunk in vector_store.raw_chunks[:5]:
            for word in chunk.split():
                if word.isalpha() and len(word) > 4:
                    topics.append(word.lower())
        topics = list(dict.fromkeys(topics))[:3]

        topic_list = (
            f"• {topics[0]}\n• {topics[1]}\n• {topics[2]}"
            if len(topics) >= 3
            else "No clear topics detected"
        )

        return (
            "⚠️ **Your question is outside the scope of this document.**\n\n"
            "👉 Please ask questions ONLY from topics present in this .txt file.\n\n"
            "This document mainly covers:\n"
            f"{topic_list}\n\n"
            "Example questions you can ask:\n"
            f"• What is {topics[0]}?\n"
            f"• Explain {topics[1]}\n"
            f"• Purpose of {topics[2]}\n\n"
            "📌 *Note: This assistant answers strictly from the uploaded document.*"
        )

    # 5) Build RAG prompt
    context = "\n\n---\n\n".join(retrieved)
    prompt = (
        "Answer ONLY using this documentation. Do NOT guess.\n\n"
        f"{context}\n\n"
        f"Question: {query}"
    )

    return llm.generate(prompt)

# LLM
llm = GroqLLMProvider()
