
import asyncio
import logging
from pathlib import Path

import pandas as pd
from openai import AsyncOpenAI
from langfuse import Langfuse

from backend.config import settings
from backend.rag.pipeline import RAGPipeline
from backend.services.ollama_client import generate_answer

from evaluation.ragas_dataset import EVALUATION_DATASET

from ragas.llms import llm_factory
from ragas.embeddings import embedding_factory

from ragas.metrics.collections import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall,
)


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

OUTPUT_PATH = Path("evaluation/ragas_results_azure.csv")

SCORE_COLUMNS = [
    "faithfulness",
    "answer_relevancy",
    "context_precision",
    "context_recall",
]


# --------------------------------------------------
# EXTRACT RETRIEVED CONTEXTS
# --------------------------------------------------

def extract_contexts(retrieved):

    contexts = []

    for item in retrieved:

        if isinstance(item, dict):

            text = (
                item.get("text")
                or item.get("chunk")
                or ""
            )

        else:

            text = getattr(
                item,
                "page_content",
                str(item)
            )

        if text:
            contexts.append(text)

    return contexts


# --------------------------------------------------
# INITIALISE LANGFUSE
# --------------------------------------------------

def initialise_langfuse():

    if not settings.LANGFUSE_PUBLIC_KEY:
        raise ValueError(
            "LANGFUSE_PUBLIC_KEY is missing."
        )

    if not settings.LANGFUSE_SECRET_KEY:
        raise ValueError(
            "LANGFUSE_SECRET_KEY is missing."
        )

    langfuse = Langfuse(
        public_key=settings.LANGFUSE_PUBLIC_KEY,
        secret_key=settings.LANGFUSE_SECRET_KEY,
        host=settings.LANGFUSE_BASE_URL,
    )

    return langfuse


# --------------------------------------------------
# MAIN EVALUATION
# --------------------------------------------------

async def main():

    print("\n" + "=" * 65)
    print("NEXUS IT - RAGAS + LANGFUSE EVALUATION")
    print("=" * 65)

    client = None
    langfuse = None

    try:

        # ------------------------------------------
        # 1. VERIFY CONFIGURATION
        # ------------------------------------------

        if not settings.AZURE_SEARCH_ENABLED:
            raise ValueError(
                "Azure AI Search is not enabled."
            )

        if not settings.FOUNDRY_ENABLED:
            raise ValueError(
                "Microsoft Foundry is not enabled."
            )

        if settings.LLM_PROVIDER.lower() != "foundry":
            raise ValueError(
                "Set LLM_PROVIDER=foundry in .env."
            )

        # ------------------------------------------
        # 2. INITIALISE LANGFUSE
        # ------------------------------------------

        langfuse = initialise_langfuse()

        print("\nLangfuse initialised successfully.")

        # ------------------------------------------
        # 3. CONNECT TO MICROSOFT FOUNDRY
        # ------------------------------------------

        client = AsyncOpenAI(
            base_url=settings.FOUNDRY_ENDPOINT.rstrip("/"),
            api_key=settings.FOUNDRY_API_KEY,
            timeout=180.0,
        )

        print("Microsoft Foundry connected.")

        # ------------------------------------------
        # 4. INITIALISE RAGAS JUDGE LLM
        # ------------------------------------------
    
        
        judge_llm = llm_factory(
    model=settings.FOUNDRY_CHAT_DEPLOYMENT,
    provider="openai",
    client=client,
    temperature=1.0,
    max_tokens=4096,
)


      


        embeddings = embedding_factory(
            "openai",
            model=settings.FOUNDRY_EMBEDDING_DEPLOYMENT,
            client=client,
        )

        # ------------------------------------------
        # 5. INITIALISE RAGAS METRICS
        # ------------------------------------------

        metrics = {
            "faithfulness": Faithfulness(
                llm=judge_llm
            ),

            "answer_relevancy": AnswerRelevancy(
                llm=judge_llm,
                embeddings=embeddings,
            ),

            "context_precision": ContextPrecision(
                llm=judge_llm
            ),

            "context_recall": ContextRecall(
                llm=judge_llm
            ),
        }

        print("RAGAS metrics initialised.")

        # ------------------------------------------
        # 6. INITIALISE AZURE RAG PIPELINE
        # ------------------------------------------

        pipeline = RAGPipeline()

        results = []

        total = len(EVALUATION_DATASET)

        # ------------------------------------------
        # 7. EVALUATE EACH QUESTION
        # ------------------------------------------

        for index, item in enumerate(
            EVALUATION_DATASET,
            start=1
        ):

            question = item["question"]
            reference = item["ground_truth"]

            print("\n" + "-" * 65)
            print(f"Question [{index}/{total}]")
            print(question)
            print("-" * 65)

            row = {
                "question": question,
                "reference": reference,
                "answer": "",
                "retrieved_context_count": 0,
                "status": "failed",
            }

            # Each evaluation question gets its own
            # Langfuse evaluation trace.

            with langfuse.start_as_current_observation(
                as_type="span",
                name="ragas-evaluation",
                input={
                    "question": question,
                    "reference": reference,
                },
            ) as evaluation_trace:

                try:

                    # ----------------------------------
                    # 7A. AZURE AI SEARCH RETRIEVAL
                    # ----------------------------------

                    retrieved = pipeline.retrieve(
                        question,
                        top_k=5
                    )

                    contexts = extract_contexts(
                        retrieved
                    )

                    row["retrieved_context_count"] = len(
                        contexts
                    )

                    if not contexts:
                        raise ValueError(
                            "Azure AI Search returned no contexts."
                        )

                    print(
                        f"Retrieved contexts: {len(contexts)}"
                    )

                    # ----------------------------------
                    # 7B. GENERATE GROUNDED ANSWER
                    # ----------------------------------

                    generation_result = generate_answer(
                        question,
                        retrieved
                    )

                    answer = generation_result["answer"]

                    row["answer"] = answer

                    print(
                        "\nGenerated answer:",
                        answer[:250]
                    )

                    # ----------------------------------
                    # 7C. PREPARE RAGAS INPUTS
                    # ----------------------------------

                    metric_inputs = {

                        "faithfulness": {
                            "user_input": question,
                            "response": answer,
                            "retrieved_contexts": contexts,
                        },

                        "answer_relevancy": {
                            "user_input": question,
                            "response": answer,
                        },

                        "context_precision": {
                            "user_input": question,
                            "reference": reference,
                            "retrieved_contexts": contexts,
                        },

                        "context_recall": {
                            "user_input": question,
                            "reference": reference,
                            "retrieved_contexts": contexts,
                        },
                    }

                    # ----------------------------------
                    # 7D. CALCULATE AND RECORD SCORES
                    # ----------------------------------

                    successful_metrics = 0

                    for metric_name, metric in metrics.items():

                        try:

                            score_result = await metric.ascore(
                                **metric_inputs[metric_name]
                            )

                            score = float(
                                score_result.value
                            )

                            row[metric_name] = score

                            reason = (
                                score_result.reason or ""
                            )

                            row[
                                f"{metric_name}_reason"
                            ] = reason

                            print(
                                f"{metric_name}: {score:.3f}"
                            )

                            # Send numerical score to Langfuse.

                            langfuse.create_score(
                                trace_id=evaluation_trace.trace_id,
                                name=metric_name,
                                value=score,
                                data_type="NUMERIC",
                                comment=reason,
                            )

                            successful_metrics += 1

                        except Exception as metric_error:

                            logger.exception(
                                "Metric %s failed",
                                metric_name
                            )

                            row[metric_name] = None

                            row[
                                f"{metric_name}_reason"
                            ] = str(metric_error)

                    # ----------------------------------
                    # 7E. UPDATE EVALUATION TRACE
                    # ----------------------------------

                    row["status"] = (
                        "success"
                        if successful_metrics == len(metrics)
                        else "partial"
                    )

                    evaluation_trace.update(
                        output={
                            "answer": answer,
                            "retrieved_context_count": len(contexts),
                            "successful_metrics": successful_metrics,
                            "total_metrics": len(metrics),
                            "status": row["status"],
                            "scores": {
                                name: row.get(name)
                                for name in SCORE_COLUMNS
                            },
                        }
                    )

                    print(
                        f"\nEvaluation status: {row['status']}"
                    )

                except Exception as error:

                    logger.exception(
                        "Evaluation failed for question"
                    )

                    row["error"] = str(error)

                    evaluation_trace.update(
                        level="ERROR",
                        status_message=str(error),
                        output={
                            "status": "failed",
                            "error": str(error),
                        },
                    )

                results.append(row)

                # Flush after each question so that
                # completed evaluations are sent.

                langfuse.flush()

        # ------------------------------------------
        # 8. SAVE RESULTS TO CSV
        # ------------------------------------------

        OUTPUT_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        df = pd.DataFrame(results)

        df.to_csv(
            OUTPUT_PATH,
            index=False
        )

        # ------------------------------------------
        # 9. DISPLAY EVALUATION SUMMARY
        # ------------------------------------------

        print("\n" + "=" * 65)
        print("NEXUS IT - RAGAS EVALUATION SUMMARY")
        print("=" * 65)

        successful = df[
            df["status"] == "success"
        ]

        partial = df[
            df["status"] == "partial"
        ]

        failed = df[
            df["status"] == "failed"
        ]

        print(f"Total questions: {total}")
        print(f"Fully evaluated: {len(successful)}")
        print(f"Partially evaluated: {len(partial)}")
        print(f"Failed: {len(failed)}")

        print("\nAverage RAGAS scores:")

        for column in SCORE_COLUMNS:

            if column in df.columns:

                average = pd.to_numeric(
                    df[column],
                    errors="coerce"
                ).mean()

                if pd.notna(average):

                    print(
                        f"{column}: {average:.3f}"
                    )

                else:

                    print(
                        f"{column}: No valid scores"
                    )

        print(
            f"\nResults saved to: {OUTPUT_PATH.resolve()}"
        )

        print(
            "\nLangfuse evaluation traces and scores submitted."
        )

    finally:

        # ------------------------------------------
        # 10. CLEAN UP
        # ------------------------------------------

        if langfuse is not None:
            langfuse.flush()

        if client is not None:
            await client.close()

        print("\nEvaluation process finished.")


# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":

    asyncio.run(main())
