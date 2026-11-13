

from backend.services.azure_indexer_service import AzureIndexerService


def test_run_indexer():
    service = AzureIndexerService()

    print("Starting Azure AI Search indexer...")

    result = service.run_indexer()

    print("Indexer trigger response:")
    print(result)


if __name__ == "__main__":
    test_run_indexer()
