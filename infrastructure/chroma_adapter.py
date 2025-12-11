import chromadb
from chromadb.config import Settings

class ChromaVectorStore:
    def __init__(self, collection_name: str, embedding_fn):
        self.embedding_fn = embedding_fn

        # Create Chroma client (new architecture)
        self.client = chromadb.PersistentClient(path="./chroma_db")

        # Create / get collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # cosine similarity recommended
        )

    def add_documents(self, docs: list[str]):
        ids = [f"id_{i}" for i in range(len(docs))]
        embeddings = [self.embedding_fn(doc) for doc in docs]

        self.collection.add(
            ids=ids,
            documents=docs,
            embeddings=embeddings
        )
    def add_texts(self, texts: list[str]):
        """Alias for compatibility with LangChain-style naming."""
        self.add_documents(texts)

    def query(self, query: str, k: int = 3):
        query_embedding = self.embedding_fn(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )

        # Return only retrieved document texts
        return results["documents"][0] if results["documents"] else []
    def similarity_search(self, query: str, k: int = 3):
        """Compatibility wrapper for LangChain-style API."""
        return self.query(query, k=k)
