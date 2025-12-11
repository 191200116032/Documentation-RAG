# infrastructure/hf_embedding_adapter.py
from sentence_transformers import SentenceTransformer

class HFEmbeddingProvider:
    def __init__(self, model="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model)

    def embed(self, text: str):
        emb = self.model.encode(text, show_progress_bar=False)
        return emb.tolist()
