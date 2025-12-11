import chromadb

class ChromaVectorStore:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name="docs",
            metadata={"hnsw:space": "cosine"}
        )
        self.raw_chunks = []

    def add_texts(self, texts):
        self.raw_chunks = texts
        ids = [str(i) for i in range(len(texts))]
        self.collection.add(ids=ids, documents=texts)

    def search(self, query, k=3):
        result = self.collection.query(query_texts=[query], n_results=k)
        return result.get("documents", [[]])[0]
