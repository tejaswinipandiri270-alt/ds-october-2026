import json
import re
from pathlib import Path

import pandas as pd
from openai import OpenAI

from backend.config import settings
from backend.rag.pipeline import RAGPipeline
from backend.services.ollama_client import generate_answer
from evaluation.ragas_dataset import EVALUATION_DATASET


# ============================================================
# 1. CONNECT TO LOCAL OLLAMA
# ============================================================

client = OpenAI(
    base_url=f"{settings.OLLAMA_BASE_URL.rstrip('/')}/v1",
    api_key="ollama"
)


# ============================================================
# 2. EXTRACT RETRIEVED CONTEXTS
# ============================================================

def extract_contexts(retrieved):
    """
    Extract text from the retrieved document chunks.
    Your existing retriever returns dictionaries containing text.
    """

    contexts = []

    for hit in retrieved:

        if isinstance(hit, dict):
            text = hit.get("text", "")

        elif hasattr(hit, "page_content"):
            text = hit.page_content

        else:
            text = str(hit)

        if text:
            contexts.append(text)

    return contexts


# ============================================================
# 3. LOCAL LLM-AS-A-JUDGE EVALUATION
# ============================================================


def evaluate_with_ollama(
    question,
    ground_truth,
    answer,
    contexts
):
    """Evaluate a RAG answer using Ollama as an LLM judge."""

    prompt = f"""
You are an independent evaluator of an Enterprise IT Support RAG system.

You must carefully compare the question, reference answer,
generated answer and retrieved contexts.

Do NOT copy example scores. You must calculate each score
from the evidence provided.

QUESTION:
{question}

REFERENCE ANSWER:
{ground_truth}

GENERATED ANSWER:
{answer}

RETRIEVED CONTEXTS:
{json.dumps(contexts, ensure_ascii=False)}

SCORING RUBRIC:

1. FAITHFULNESS
Measure whether claims in the generated answer are supported
by the retrieved contexts.
1.0 = All important claims are supported.
0.5 = Some claims are supported, others are unsupported.
0.0 = The answer is unsupported or contradicts the contexts.

2. ANSWER RELEVANCY
Measure whether the generated answer addresses the question.
1.0 = Directly and completely answers the question.
0.5 = Partially answers the question.
0.0 = Does not answer the question.

3. CONTEXT PRECISION
Measure how much of the retrieved context is relevant
to answering the question.
1.0 = All retrieved contexts are relevant.
0.5 = Some retrieved contexts are relevant.
0.0 = None of the retrieved contexts are relevant.

4. CONTEXT RECALL
Compare the retrieved contexts against the reference answer.
1.0 = Context contains all important information needed.
0.5 = Context contains some important information.
0.0 = Context contains none of the required information.

IMPORTANT:
- Evaluate each metric independently.
- Do not automatically assign zero.
- Do not automatically assign one.
- Use the actual evidence, not assumptions.
- Give a short explanation for every score.
- The score must be a number between 0 and 1.

Return valid JSON only, with no Markdown:

{{
  "faithfulness": {{
    "score": 0.0,
    "reason": "Explain the evidence."
  }},
  "answer_relevancy": {{
    "score": 0.0,
    "reason": "Explain the evidence."
  }},
  "context_precision": {{
    "score": 0.0,
    "reason": "Explain the evidence."
  }},
  "context_recall": {{
    "score": 0.0,
    "reason": "Explain the evidence."
  }}
}}
"""

    response = client.chat.completions.create(
        model=settings.OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    content = response.choices[0].message.content

    print("\nRAW OLLAMA EVALUATION:")
    print(content)

    if not content:
        raise ValueError("Ollama returned an empty response.")

    match = re.search(r"\{[\s\S]*\}", content)

    if not match:
        raise ValueError("Ollama did not return valid JSON.")

    evaluation = json.loads(match.group())

    required_metrics = [
        "faithfulness",
        "answer_relevancy",
        "context_precision",
        "context_recall"
    ]

    scores = {}

    for metric in required_metrics:

        if metric not in evaluation:
            raise ValueError(f"Missing metric: {metric}")

        metric_result = evaluation[metric]

        if not isinstance(metric_result, dict):
            raise ValueError(
                f"Invalid response structure for {metric}"
            )

        value = float(metric_result["score"])
        reason = str(metric_result.get("reason", ""))

        if not 0 <= value <= 1:
            raise ValueError(
                f"Invalid score for {metric}: {value}"
            )

        scores[metric] = value

        print(f"\n{metric}: {value:.2f}")
        print("Reason:", reason)

    return scores


# ============================================================
# 4. MAIN EVALUATION PIPELINE
# ============================================================

def main():

    print("\n" + "=" * 60)
    print("ENTERPRISE IT SUPPORT RAG EVALUATION")
    print("=" * 60)

    print("\nEvaluation model:", settings.OLLAMA_MODEL)

    # Initialise the existing RAG pipeline
    pipeline = RAGPipeline()

    # Check whether the vector database contains documents
    if not pipeline.store.count():

        print("\nKnowledge base is empty.")
        print("Ingesting documents...")

        ingestion_result = pipeline.ingest_directory()

        print("Ingestion completed:", ingestion_result)

    results = []

    total_questions = len(EVALUATION_DATASET)

    # --------------------------------------------------------
    # Evaluate each question
    # --------------------------------------------------------

    for index, item in enumerate(
        EVALUATION_DATASET,
        start=1
    ):

        question = item["question"]
        ground_truth = item["ground_truth"]

        print("\n" + "-" * 60)
        print(f"QUESTION {index}/{total_questions}")
        print("-" * 60)

        print("Question:", question)

        try:

            # Step 1: Retrieve relevant chunks
            retrieved = pipeline.retrieve(
                question,
                top_k=5
            )

            # Step 2: Extract retrieved context text
            contexts = extract_contexts(retrieved)

            print("Retrieved chunks:", len(contexts))
            print("\nREFERENCE ANSWER:")
            print(ground_truth)

            print("\nRETRIEVED CONTEXTS:")
            for i, context in enumerate(contexts, start=1):
                print(f"\n--- Context {i} ---")
                print(context)


            # Step 3: Generate answer using existing Ollama client
            answer = generate_answer(
                question,
                retrieved
            )

            print("\nGenerated answer:")
            print(answer[:300])

            # Step 4: Evaluate generated answer
            scores = evaluate_with_ollama(
                question=question,
                ground_truth=ground_truth,
                answer=answer,
                contexts=contexts
            )

            # Step 5: Store results
            result = {
                "question": question,
                "ground_truth": ground_truth,
                "answer": answer,
                "faithfulness": scores["faithfulness"],
                "answer_relevancy": scores["answer_relevancy"],
                "context_precision": scores["context_precision"],
                "context_recall": scores["context_recall"],
                "status": "success"
            }

            results.append(result)

            print("\nEvaluation scores:")

            for metric, score in scores.items():
                print(f"{metric}: {score:.2f}")

        except Exception as error:

            print("\nEvaluation failed:")
            print(str(error))

            results.append({
                "question": question,
                "ground_truth": ground_truth,
                "answer": "",
                "faithfulness": None,
                "answer_relevancy": None,
                "context_precision": None,
                "context_recall": None,
                "status": f"failed: {error}"
            })

    # ========================================================
    # 5. SAVE RESULTS
    # ========================================================

    output_path = Path("evaluation/ragas_results.csv")

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df = pd.DataFrame(results)

    df.to_csv(
        output_path,
        index=False
    )

    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)

    successful = df[df["status"] == "success"]

    if not successful.empty:

        metric_columns = [
            "faithfulness",
            "answer_relevancy",
            "context_precision",
            "context_recall"
        ]

        print("\nAverage Evaluation Scores:")

        average_scores = successful[
            metric_columns
        ].mean()

        print(average_scores.round(3).to_string())

        print(
            f"\nSuccessfully evaluated: "
            f"{len(successful)}/{total_questions}"
        )

    else:

        print("\nNo questions were successfully evaluated.")

    print("\nResults saved to:", output_path)

    print("\nEvaluation completed.")


# ============================================================
# 6. EXECUTION
# ============================================================

if __name__ == "__main__":
    main()