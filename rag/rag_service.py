import json
import re
from pathlib import Path
from collections import Counter


class RAGService:
    """
    Lightweight RAG service designed for low-memory deployment.

    Retrieves relevant knowledge documents using token-based
    similarity and supplies them as grounding context to Gemini.
    """

    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent

        self.data_files = [
            self.project_root / "data" / "supply_chain_data.json",
            self.project_root / "data" / "risk_scenarios.json",
            self.project_root / "data" / "alternative_routes.json",
        ]

        self.documents = []
        self.document_texts = []

        self.load_documents()

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

            document_text = json.dumps(
                data,
                ensure_ascii=False,
            )

            self.document_texts.append(document_text)

        return self.documents

    # ============================================================
    # TOKENIZE TEXT
    # ============================================================

    def _tokenize(self, text):

        return re.findall(
            r"\b[a-zA-Z0-9]+\b",
            text.lower(),
        )

    # ============================================================
    # CALCULATE DOCUMENT RELEVANCE
    # ============================================================

    def _calculate_score(
        self,
        query,
        document_text,
    ):

        query_tokens = Counter(
            self._tokenize(query)
        )

        document_tokens = Counter(
            self._tokenize(document_text)
        )

        score = 0

        for token, count in query_tokens.items():

            if token in document_tokens:
                score += min(
                    count,
                    document_tokens[token],
                )

        return float(score)

    # ============================================================
    # RETRIEVE RELEVANT KNOWLEDGE
    # ============================================================

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ):

        if not self.documents:
            return []

        scored_documents = []

        for document, document_text in zip(
            self.documents,
            self.document_texts,
        ):

            score = self._calculate_score(
                query,
                document_text,
            )

            scored_documents.append(
                {
                    "source": document["source"],
                    "score": score,
                    "content": document["content"],
                }
            )

        scored_documents.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return scored_documents[:top_k]


rag_service = RAGService()