
from backend.config import settings
from backend.rag.pipeline import RAGPipeline


def test_rag_pipeline(monkeypatch):

    class FakeAzureRetriever:

        def __init__(self):
            pass

        def hybrid_search(self, question, top_k):
            return {
                "count": 1,
                "results": [
                    {
                        "id": "chunk-1",
                        "title": "Outlook Support Guide",
                        "text": (
                            "Check your internet connection and "
                            "Outlook account settings."
                        ),
                        "rerank_score": 0.95
                    }
                ]
            }

    monkeypatch.setattr(settings, "AZURE_SEARCH_ENABLED", True)

    monkeypatch.setattr(
        "backend.rag.pipeline.AzureSearchRetriever",
        FakeAzureRetriever
    )

    pipeline = RAGPipeline()

    question = "How do I troubleshoot Outlook email issues?"

    results = pipeline.retrieve(question, top_k=3)

    assert len(results) == 1
    assert results[0]["title"] == "Outlook Support Guide"
    assert "Outlook account settings" in results[0]["text"]