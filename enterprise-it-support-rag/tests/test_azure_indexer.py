from backend.config import settings
from backend.services import azure_indexer_service


class FakeIndexerClient:
    def __init__(self, endpoint, credential):
        self.endpoint = endpoint
        self.credential = credential

    def run_indexer(self, indexer_name):
        self.indexer_name = indexer_name


def test_run_indexer(monkeypatch):
    monkeypatch.setattr(settings, "AZURE_SEARCH_ENDPOINT", "https://test.search.windows.net")
    monkeypatch.setattr(settings, "AZURE_SEARCH_ADMIN_KEY", "test-admin-key")
    monkeypatch.setattr(
        azure_indexer_service,
        "SearchIndexerClient",
        FakeIndexerClient,
    )

    service = azure_indexer_service.AzureIndexerService()
    result = service.run_indexer()

    assert result["status"] == "triggered"
    assert result["indexer"] == "rag-1794563417722-indexer"
