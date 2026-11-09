import json
from pathlib import Path

from backend.rag.pipeline import RAGPipeline


def main():
    project_root = Path(__file__).resolve().parents[2]
    dataset_path = Path(__file__).with_name("final_test_questions.json")

    with dataset_path.open("r", encoding="utf-8-sig") as file:
        questions = json.load(file)

    pipeline = RAGPipeline()

    if pipeline.store.count() == 0:
        print("Knowledge base is empty. Run ingestion first.")
        return

    hits_at_3 = 0
    hits_at_5 = 0
    reciprocal_ranks = []

    print("\nFINAL RETRIEVAL EVALUATION")
    print("=" * 65)

    for index, item in enumerate(questions, start=1):
        question = item["question"]
        expected_source = item["expected_source"]

        results = pipeline.retrieve(question, top_k=5)

        retrieved_sources = [
            result.get("metadata", {}).get("filename", "")
            for result in results
        ]

        rank = next(
            (
                position
                for position, filename in enumerate(retrieved_sources, start=1)
                if filename == expected_source
            ),
            None
        )

        if rank is not None:
            reciprocal_ranks.append(1 / rank)
            if rank <= 3:
                hits_at_3 += 1
            if rank <= 5:
                hits_at_5 += 1
        else:
            reciprocal_ranks.append(0)

        print(f"\nTest {index}: {question}")
        print("Expected:", expected_source)
        print("Retrieved:", retrieved_sources)
        print("Expected source rank:", rank if rank else "Not found")

    total = len(questions)

    hit_at_3 = hits_at_3 / total
    hit_at_5 = hits_at_5 / total
    mrr = sum(reciprocal_ranks) / total

    print("\n" + "=" * 65)
    print("FINAL METRICS")
    print("=" * 65)
    print(f"Total questions: {total}")
    print(f"Hit@3: {hit_at_3:.3f} ({hits_at_3}/{total})")
    print(f"Hit@5: {hit_at_5:.3f} ({hits_at_5}/{total})")
    print(f"MRR@5: {mrr:.3f}")


if __name__ == "__main__":
    main()
