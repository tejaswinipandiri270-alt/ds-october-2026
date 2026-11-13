from azure.search.documents.models import VectorizableTextQuery
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from backend.config import settings


class AzureSearchRetriever:
    """Retrieve IT support document chunks from Azure AI Search."""

    def __init__(self):
        if not settings.AZURE_SEARCH_ENDPOINT:
            raise ValueError("AZURE_SEARCH_ENDPOINT is missing from .env")

        if not settings.AZURE_SEARCH_API_KEY:
            raise ValueError("AZURE_SEARCH_API_KEY is missing from .env")

        self.client = SearchClient(
            endpoint=settings.AZURE_SEARCH_ENDPOINT,
            index_name=settings.AZURE_SEARCH_INDEX_NAME,
            credential=AzureKeyCredential(
                settings.AZURE_SEARCH_API_KEY
            ),
        )

    def normalise_results(self, results):
        """Convert Azure documents into the local RAG format."""

        documents = []

        for result in results:
            document = dict(result)

            document["id"] = document.get("chunk_id")
            document["text"] = document.get("chunk", "")

            documents.append(document)

        return documents

    def search(self, query: str, top_k: int = 5):
        """Run a keyword search and return matching documents."""

        results = self.client.search(
            search_text=query,
            top=top_k,
            include_total_count=True,
        )

        documents = []

        for result in results:
            document = dict(result)
            document["@search.score"] = result.get("@search.score")
            documents.append(document)

        return {
            "count": len(documents),
            "results": documents,
        }
    def vector_search(self, query: str, top_k: int = 5):
        """Run vector search using Azure integrated vectorization."""

        vector_query = VectorizableTextQuery(
            text=query,
            k_nearest_neighbors=top_k,
            fields="text_vector",
        )

        results = self.client.search(
            search_text=None,
            vector_queries=[vector_query],
            top=top_k,
        )

        documents = []

        for result in results:
            documents.append(dict(result))

        return {
            "count": len(documents),
            "results": documents,
        }
    
    
    def hybrid_search(self, query: str, top_k: int = 5):
        """Combine Azure keyword and vector search."""

        vector_query = VectorizableTextQuery(
            text=query,
            k_nearest_neighbors=top_k,
            fields="text_vector",
        )

        results = self.client.search(
            search_text=query,
            vector_queries=[vector_query],
            select=["chunk_id", "parent_id", "chunk", "title"],
            top=top_k,
        )

        documents = self.normalise_results(results)

        return {
            "count": len(documents),
            "results": documents,
        }
