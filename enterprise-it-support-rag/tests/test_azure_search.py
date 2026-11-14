from backend.config import settings
from backend.rag import azure_search_retriever


class FakeSearchClient:
    """Simulate Azure Search without network access."""

    def __init__(self, **kwargs):
        self.endpoint = kwargs["endpoint"]
        self.index_name = kwargs["index_name"]

    def search(self, **kwargs):
        return [
            {
                "chunk_id": "chunk-1",
                "parent_id": "document-1",
                "chunk": "Reset your password using the IT support portal.",
                "title": "Password Reset Guide",
                "@search.score": 0.95,
            }
        ]


def setup_fake_search(monkeypatch):
    monkeypatch.setattr(
        settings,
        "AZURE_SEARCH_ENDPOINT",
        "https://test.search.windows.net",
    )
    monkeypatch.setattr(
        settings,
        "AZURE_SEARCH_API_KEY",
        "test-api-key",
    )
    monkeypatch.setattr(
        azure_search_retriever,
        "SearchClient",
        FakeSearchClient,
    )


def test_vector_search(monkeypatch):
    setup_fake_search(monkeypatch)

    retriever = azure_search_retriever.AzureSearchRetriever()
    result = retriever.vector_search(
        "How do I reset my password?",
        top_k=3,
    )

    assert result["count"] == 1
    assert result["results"][0]["title"] == "Password Reset Guide"


def test_hybrid_search(monkeypatch):
    setup_fake_search(monkeypatch)

    retriever = azure_search_retriever.AzureSearchRetriever()
    result = retriever.hybrid_search(
        "How do I reset my password?",
        top_k=3,
    )

    assert result["count"] == 1
    assert result["results"][0]["id"] == "chunk-1"
    assert "Reset your password" in result["results"][0]["text"]
