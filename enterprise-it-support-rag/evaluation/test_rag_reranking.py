from backend.rag.pipeline import RAGPipeline


def main():
    print("Starting RAG Hybrid Retrieval + Reranking Test")

    pipeline = RAGPipeline()

    question = "How can an employee reset a forgotten password?"

    print("\nQuestion:", question)
    print("\nRetrieving and reranking documents...")

    results = pipeline.retrieve(question, top_k=3)

    print("\nFINAL RERANKED RESULTS")
    print("=" * 60)

    for rank, document in enumerate(results, start=1):
        metadata = document.get("metadata", {})

        print(f"\nRank: {rank}")
        print("Source:", metadata.get("filename", "Unknown"))
        print("Rerank score:", round(document.get("rerank_score", 0), 4))
        print("Content:", document["text"][:300])


if __name__ == "__main__":
    main()