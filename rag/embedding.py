# # rag/embedding.py
# from sentence_transformers import SentenceTransformer
# import numpy as np
# import threading
#
# _model = None
# _lock = threading.Lock()
#
# def _get_model():
#     global _model
#     with _lock:
#         if _model is None:
#             # lightweight local embedding model
#             _model = SentenceTransformer("all-MiniLM-L6-v2")
#         return _model
#
# def embed_texts(texts):
#     """
#     texts: list[str]
#     returns: numpy.ndarray shape (n, d) normalized
#     """
#     model = _get_model()
#     arr = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
#     return arr
#
# def embed_text(text):
#     return embed_texts([text])[0]
