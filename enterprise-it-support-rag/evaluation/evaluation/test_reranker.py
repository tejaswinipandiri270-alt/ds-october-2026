from backend.rag.reranker import CrossEncoderReranker


def main():
    print("Starting Cross-Encoder Reranker Test...")

    reranker = CrossEncoderReranker()

    question = "How can I reset my forgotten password?"

    documents = [
        {"id": "1", "text": "Employees can reset forgotten passwords using the approved self-service password reset portal."},
        {"id": "2", "text": "Employees should report suspicious emails to the IT security team."},
        {"id": "3", "text": "Multi-Factor Authentication is required when verifying employee identity."},
        {"id": "4", "text": "The company VPN allows employees to access internal systems remotely."}
    ]

    results = reranker.rerank(
        query=question,
        documents=documents,
        top_k=3
    )

    print("\nCROSS-ENCODER RERANKING RESULTS")
    print("=" * 60)

    for rank, document in enumerate(results, start=1):
        print(f"\nRank: {rank}")
        print("Document:", document["text"])
        print("Relevance score:", round(document["rerank_score"], 4))


if __name__ == "__main__":
    main()
