import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class RAGService:

    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent

        self.data_files = [
            self.project_root / "data" / "supply_chain_data.json",
            self.project_root / "data" / "risk_scenarios.json",
            self.project_root / "data" / "alternative_routes.json",
        ]

        # Documents used by the vector database
        self.documents = []

        # Text representation of each document
        self.document_texts = []

        # Sentence Transformer embedding model
        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        # FAISS vector index
        self.index = None

        self.load_documents()
        self.build_vector_index()

    # ============================================================
    # LOAD KNOWLEDGE DOCUMENTS
    # ============================================================

    def load_documents(self):
        self.documents = []
        self.document_texts = []

        for file_path in self.data_files:

            if not file_path.exists():
                continue

            with open(
                file_path,
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            document = {
                "source": file_path.name,
                "content": data,
            }

            self.documents.append(document)

            # Convert JSON knowledge into text for embedding
            document_text = json.dumps(
                data,
                ensure_ascii=False,
            )

            self.document_texts.append(document_text)

        return self.documents

    # ============================================================
    # BUILD FAISS VECTOR INDEX
    # ============================================================

    def build_vector_index(self):

        if not self.document_texts:
            self.index = None
            return

        embeddings = self.embedding_model.encode(
            self.document_texts,
            convert_to_numpy=True,
        )

        embeddings = np.asarray(
            embeddings,
            dtype="float32",
        )

        # Normalize vectors so inner product acts as cosine similarity
        faiss.normalize_L2(embeddings)

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(embeddings)

    # ============================================================
    # SEMANTIC RETRIEVAL
    # ============================================================

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ):

        if self.index is None:
            return []

        query_embedding = self.embedding_model.encode(
            [query],
            convert_to_numpy=True,
        )

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32",
        )

        faiss.normalize_L2(query_embedding)

        number_of_results = min(
            top_k,
            len(self.documents),
        )

        scores, indices = self.index.search(
            query_embedding,
            number_of_results,
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0],
        ):

            if index == -1:
                continue

            document = self.documents[index]

            results.append({
                "source": document["source"],
                "score": float(score),
                "content": document["content"],
            })

        return results


rag_service = RAGService()