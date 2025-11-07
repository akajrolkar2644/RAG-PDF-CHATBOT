import os, pickle, faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from backend.config.settings import VECTOR_STORE_PATH, MODEL_NAME

class VectorStore:
    def __init__(self):
        os.makedirs(VECTOR_STORE_PATH, exist_ok=True)
        self.index_file = os.path.join(VECTOR_STORE_PATH, "index.faiss")
        self.meta_file = os.path.join(VECTOR_STORE_PATH, "meta.pkl")
        self.model = SentenceTransformer(MODEL_NAME)
        self.dim = self.model.get_sentence_embedding_dimension()
        if os.path.exists(self.index_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.meta_file, "rb") as f:
                self.metadata = pickle.load(f)
        else:
            self.index = faiss.IndexFlatIP(self.dim)
            self.metadata = []

    def _embed(self, texts):
        return self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)

    def add_documents(self, docs_meta):
        texts = [d["text"] for d in docs_meta]
        vectors = self._embed(texts)
        self.index.add(vectors)  # type: ignore[reportCallIssue]
        self.metadata.extend(docs_meta)
        self._persist()

    def similarity_search(self, query, top_k=5):
        vec = self._embed([query])
        scores, idxs = self.index.search(vec, top_k)  # type: ignore[reportCallIssue]
        return [self.metadata[i] for i in idxs[0] if i < len(self.metadata)]

    def _persist(self):
        faiss.write_index(self.index, self.index_file)
        with open(self.meta_file, "wb") as f:
            pickle.dump(self.metadata, f)