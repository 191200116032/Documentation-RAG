# infrastructure/chroma_adapter.py
import os
from typing import List
import chromadb
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
import numpy as np


class ChromaVectorStore:
    def __init__(self, persist_directory: str = "./chroma_data", collection_name: str = "docs"):
        self.persist_directory = persist_directory
        self.collection_name = collection_name

        # Ensure directory exists
        os.makedirs(persist_directory, exist_ok=True)

        # ✅ New Chroma client (safe, recommended)
        self.client = PersistentClient(path=persist_directory)

        # Create or load collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # optional, but good
        )

        # Load local embedding model
        self.embed_model = SentenceTransformer("all-MiniLM-L6-v2")

    def _embed_texts(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.embed_model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False
        )
        return embeddings.tolist()

    def add_documents(self, texts: List[str], ids: List[str]):
        embeddings = self._embed_texts(texts)
        self.collection.add(
            documents=texts,
            ids=ids,
            embeddings=embeddings
        )

    def similarity_search(self, query: str, k: int = 3) -> List[str]:
        q_emb = self._embed_texts([query])[0]
        results = self.collection.query(
            query_embeddings=[q_emb],
            n_results=k
        )
        return results.get("documents", [[]])[0]

    def reset(self):
        """Delete and recreate the collection."""
        try:
            self.client.delete_collection(self.collection_name)
        except Exception:
            pass

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
