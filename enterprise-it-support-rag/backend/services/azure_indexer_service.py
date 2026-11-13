
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexerClient

from backend.config import settings


class AzureIndexerService:

    def __init__(self):
        if not settings.AZURE_SEARCH_ENDPOINT:
            raise ValueError("Azure Search endpoint is missing")

        if not settings.AZURE_SEARCH_ADMIN_KEY:
            raise ValueError("Azure Search admin key is missing")

        self.client = SearchIndexerClient(
            endpoint=settings.AZURE_SEARCH_ENDPOINT,
            credential=AzureKeyCredential(
                settings.AZURE_SEARCH_ADMIN_KEY
            )
        )
        self.indexer_name = "rag-1794563417722-indexer"

    def run_indexer(self):
        """Trigger the existing Azure AI Search indexer."""

        self.client.run_indexer(self.indexer_name)

        return {
            "indexer": self.indexer_name,
            "status": "triggered"
        }

    def get_indexer_status(self):
        """Get the latest indexer execution status."""

        status = self.client.get_indexer_status(
            self.indexer_name
        )

        return {
            "indexer": self.indexer_name,
            "status": status.status,
            "last_result": (
                status.last_result.status
                if status.last_result
                else None
            )
        }
