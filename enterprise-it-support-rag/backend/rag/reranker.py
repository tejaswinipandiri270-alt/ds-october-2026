from sentence_transformers import CrossEncoder


class CrossEncoderReranker:

    def __init__(
        self,
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):
        print("Loading Cross-Encoder model...")
        self.model = CrossEncoder(model_name)
        print("Cross-Encoder model loaded successfully.")

    def rerank(self, query, documents, top_k=3):

        if not documents:
            return []

        pairs = [
            (query, document["text"])
            for document in documents
        ]

        scores = self.model.predict(pairs)

        reranked_documents = []

        for document, score in zip(documents, scores):
            updated_document = dict(document)
            updated_document["rerank_score"] = float(score)
            reranked_documents.append(updated_document)

        reranked_documents.sort(
            key=lambda item: item["rerank_score"],
            reverse=True
        )

        return reranked_documents[:top_k]
