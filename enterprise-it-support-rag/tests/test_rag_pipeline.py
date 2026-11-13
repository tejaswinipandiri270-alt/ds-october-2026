
from backend.rag.pipeline import RAGPipeline


def test_rag_pipeline():

    print("\nInitialising RAG Pipeline...")

    pipeline = RAGPipeline()

    question = "How do I troubleshoot Outlook email issues?"

    print("\nQuestion:", question)

    results = pipeline.retrieve(
        question,
        top_k=3
    )

    print("\nFinal Reranked Results:")

    for i, result in enumerate(results, start=1):

        print(f"\nResult {i}")
        print("Source:", result.get("title"))
        print("Rerank Score:", result.get("rerank_score"))
        print("Content:", result.get("text", "")[:400])

    print("\nRAG Pipeline retrieval test completed!")


if __name__ == "__main__":
    test_rag_pipeline()
