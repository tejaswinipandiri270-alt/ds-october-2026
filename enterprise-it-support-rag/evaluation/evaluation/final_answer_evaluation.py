
import json
import requests
from pathlib import Path

from backend.rag.pipeline import RAGPipeline
from backend.services.ollama_client import generate_answer
from backend.config import settings


def judge_answer(question, expected_answer, answer, contexts):
    context_text = "\n\n".join(
        item["text"] for item in contexts
    )

    prompt = f"""
You are an expert evaluator of Retrieval-Augmented Generation systems.

Evaluate the generated answer fairly using the retrieved context.

QUESTION:
{question}

REFERENCE ANSWER:
{expected_answer}

RETRIEVED CONTEXT:
{context_text}

GENERATED ANSWER:
{answer}

SCORING RUBRIC:

FAITHFULNESS:
5 = All factual claims are supported by the retrieved context.
4 = Mostly supported, with only minor unsupported details.
3 = Partially supported.
2 = Mostly unsupported.
1 = Contradicts or is unrelated to the context.

ANSWER RELEVANCE:
5 = Directly and completely answers the question.
4 = Answers the question with minor omissions.
3 = Partially answers the question.
2 = Mostly irrelevant.
1 = Does not answer the question.

CONTEXT PRECISION:
5 = All retrieved chunks are relevant to the question.
4 = Most chunks are relevant.
3 = A mixture of relevant and irrelevant chunks.
2 = Mostly irrelevant chunks.
1 = Retrieved chunks do not support the question.

CONTEXT RECALL:
5 = Context contains all information needed for a complete answer.
4 = Context contains nearly all necessary information.
3 = Context contains some necessary information.
2 = Context contains very little necessary information.
1 = Context contains none of the required information.

IMPORTANT:
- Accept accurate paraphrasing.
- Do not require exact wording from the reference answer.
- Do not penalise concise answers that contain the necessary information.
- Judge context precision using the retrieved context, not the generated answer.
- Judge context recall by comparing the reference answer with the retrieved context.
- Do not automatically give low scores.
- Do not automatically give high scores.
- Evaluate each metric independently.
- Explain every score briefly.

Return ONLY valid JSON using this structure:
{{
    "faithfulness": 1,
    "answer_relevance": 1,
    "context_precision": 1,
    "context_recall": 1,
    "reason": "Brief explanation of the scores."
}}
"""

    response = requests.post(
        f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/generate",
        json={
            "model": settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {"temperature": 0}
        },
        timeout=settings.OLLAMA_TIMEOUT
    )

    response.raise_for_status()

    scores = json.loads(
        response.json().get("response", "")
    )

    metrics = [
        "faithfulness",
        "answer_relevance",
        "context_precision",
        "context_recall"
    ]

    for metric in metrics:
        value = scores.get(metric)

        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not 1 <= value <= 5
        ):
            raise ValueError(
                f"Invalid evaluation score: {metric}={value}"
            )

    if not isinstance(scores.get("reason"), str):
        raise ValueError("Judge did not return an explanation.")

    return scores


def main():
    dataset_path = Path(__file__).with_name(
        "final_answer_test.json"
    )

    with dataset_path.open(
        "r", encoding="utf-8-sig"
    ) as file:
        dataset = json.load(file)

    pipeline = RAGPipeline()

    if pipeline.store.count() == 0:
        print("Knowledge base is empty. Run ingestion first.")
        return

    metrics = [
        "faithfulness",
        "answer_relevance",
        "context_precision",
        "context_recall"
    ]

    totals = {metric: 0 for metric in metrics}
    results = []

    print("\nFINAL ANSWER QUALITY EVALUATION")
    print("=" * 60)

    for index, item in enumerate(dataset, start=1):
        question = item["question"]
        expected = item["expected_answer"]

        print(f"\nTest {index}/{len(dataset)}: {question}")

        contexts = pipeline.retrieve(question, top_k=5)

        answer = generate_answer(question, contexts)

        scores = judge_answer(
            question,
            expected,
            answer,
            contexts
        )

        for metric in metrics:
            totals[metric] += scores[metric]

        results.append({
            "question": question,
            "expected_answer": expected,
            "generated_answer": answer,
            "scores": scores
        })

        print("\nGenerated answer:")
        print(answer)

        print("\nEvaluation scores:")
        for metric in metrics:
            print(f"{metric}: {scores[metric]}/5")

        print("Reason:", scores["reason"])

    total = len(dataset)

    print("\n" + "=" * 60)
    print("AVERAGE ANSWER QUALITY SCORES")
    print("=" * 60)

    for metric in metrics:
        print(f"{metric}: {totals[metric] / total:.2f}/5")

    output_path = Path(__file__).with_name(
        "final_answer_evaluation_results.json"
    )

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nDetailed results saved to:")
    print(output_path)

    print(
        "\nNote: These are local LLM-judge estimates, "
        "not official RAGAS scores."
    )


if __name__ == "__main__":
    main()
