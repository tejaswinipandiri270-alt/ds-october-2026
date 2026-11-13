
from backend.rag.azure_search_retriever import AzureSearchRetriever

def main():
    print("Connecting to Azure AI Search...")

    retriever = AzureSearchRetriever()

    question = "How do I troubleshoot Outlook email issues?"

    print(f"\nQuestion: {question}")

    response = retriever.search(question, top_k=3)

    print(f"\nMatching documents: {response['count']}")

    for i, document in enumerate(response["results"], start=1):
        print(f"\nResult {i}")
        print("Available fields:", list(document.keys()))
        print("Score:", document.get("@search.score"))
        print("Content:", document.get("chunk", "No chunk field found")[:500])


from backend.rag.azure_search_retriever import AzureSearchRetriever


def test_vector_search():
    print("\nTesting Azure Vector Search...")

    retriever = AzureSearchRetriever()

    # Enter your question here
    response = retriever.vector_search(
        "My Outlook is not receiving emails. What should I do?",
        top_k=3
    )

    print(f"\nMatching documents: {response['count']}")

    for i, document in enumerate(response["results"], start=1):
        print(f"\nResult {i}")
        print("Title:", document.get("title"))
        print("Score:", document.get("@search.score"))
        print("Content:", document.get("chunk", "")[:500])





def test_hybrid_search():
    print("\nTesting Azure Hybrid Search...")

    retriever = AzureSearchRetriever()

    question = "My Outlook is not receiving emails. What should I do?"

    response = retriever.hybrid_search(question, top_k=5)

    print(f"\nMatching documents: {response['count']}")

    for i, document in enumerate(response["results"], start=1):
        print(f"\nResult {i}")
        print("Title:", document.get("title"))
        print("Score:", document.get("@search.score"))
        print("Content:", document.get("chunk", "")[:500])
if __name__ == "__main__":
    test_hybrid_search()