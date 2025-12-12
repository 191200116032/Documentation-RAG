# # rag/vector_store.py
# import numpy as np
# from rag.embedding import embed_texts, embed_text
#
# class InMemoryVectorStore:
#     def __init__(self):
#         self.docs = []          # list[str]
#         self.embeddings = None  # numpy array (n x d)
#
#     def add_texts(self, texts):
#         if not texts:
#             return
#         vecs = embed_texts(texts)  # normalized
#         if self.embeddings is None:
#             self.embeddings = vecs
#         else:
#             self.embeddings = np.vstack([self.embeddings, vecs])
#         self.docs.extend(texts)
#
#     def similarity_search(self, query, k=3):
#         if not self.docs or self.embeddings is None:
#             return []
#         qv = embed_text(query)  # normalized
#         sims = np.dot(self.embeddings, qv)  # cosine since normalized
#         idx = np.argsort(-sims)[:k]
#         return [self.docs[i] for i in idx if i < len(self.docs)]
#
#     def clear(self):
#         self.docs = []
#         self.embeddings = None
