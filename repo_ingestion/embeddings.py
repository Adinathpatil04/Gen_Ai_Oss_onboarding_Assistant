from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import torch

class CodeEmbeddingStore:
    def __init__(self):
        # 🔥 Force eager weight loading (NO meta tensors)
        torch.set_default_dtype(torch.float32)

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            device="cpu",
            trust_remote_code=False
        )

        self.index = None
        self.metadata = []

    def add_embeddings(self, texts, meta):
        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True
        ).astype("float32")

        if self.index is None:
            self.index = faiss.IndexFlatL2(embeddings.shape[1])

        self.index.add(embeddings)
        self.metadata.extend(meta)

    def search(self, query, top_k=5):
        query_vec = self.model.encode(
            [query],
            convert_to_numpy=True
        ).astype("float32")

        _, indices = self.index.search(query_vec, top_k)
        return [self.metadata[i] for i in indices[0]]

    def search_with_scores(self, query, top_k=5):
        query_vec = self.model.encode(
            [query],
            convert_to_numpy=True
        ).astype("float32")

        distances, indices = self.index.search(query_vec, top_k)

        return [
            {"score": float(d), "meta": self.metadata[i]}
            for d, i in zip(distances[0], indices[0])
        ]
