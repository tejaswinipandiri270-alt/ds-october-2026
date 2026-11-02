"""Manual calibration helper. Fill your own ratings, then compare with judge ratings.
The app's judge output can be copied into the judge_scores column for 10 examples.
This script deliberately does not invent calibration results.
"""

"""Compare human ratings with LLM judge ratings."""

import csv
from pathlib import Path

FIELDS = [
    "question_answering_score",
    "tone_score",
    "policy_compliance_score",
]


def main():
    path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "judge_calibration.csv"
    )

    if not path.exists():
        raise SystemExit(
            "Create data/judge_calibration.csv first."
        )

    with path.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    if len(rows) < 10:
        raise SystemExit(
            f"Need at least 10 examples; found {len(rows)}."
        )

    total_matches = 0
    total_comparisons = 0
    total_difference = 0
    complete_examples = 0

    field_results = {
        field: {"matches": 0, "count": 0, "difference": 0}
        for field in FIELDS
    }

    for row in rows:
        example_complete = True

        for field in FIELDS:
            human_value = row.get("human_" + field, "").strip()
            judge_value = row.get("judge_" + field, "").strip()

            if not human_value or not judge_value:
                example_complete = False
                continue

            try:
                human = int(human_value)
                judge = int(judge_value)
            except ValueError:
                raise SystemExit(
                    f"Invalid score in example {row.get('example_id', '?')}."
                )

            if human not in range(1, 6) or judge not in range(1, 6):
                raise SystemExit("All scores must be between 1 and 5.")

            difference = abs(human - judge)
            match = human == judge

            total_comparisons += 1
            total_matches += int(match)
            total_difference += difference

            result = field_results[field]
            result["count"] += 1
            result["matches"] += int(match)
            result["difference"] += difference

        if example_complete:
            complete_examples += 1

    if complete_examples < 10:
        raise SystemExit(
            f"Need 10 examples with all six ratings completed. "
            f"Found {complete_examples}."
        )

    print("\nHUMAN vs LLM JUDGE RESULTS")
    print("-------------------------")

    agreement = 100 * total_matches / total_comparisons
    average_difference = total_difference / total_comparisons

    print(f"Complete examples: {complete_examples}")
    print(
        f"Exact agreement: {total_matches}/{total_comparisons} "
        f"= {agreement:.1f}%"
    )
    print(f"Average absolute difference: {average_difference:.2f}")

    print("\nAGREEMENT BY CRITERION")
    for field, result in field_results.items():
        count = result["count"]
        if count:
            percentage = 100 * result["matches"] / count
            avg_diff = result["difference"] / count
            print(
                f"{field}: {percentage:.1f}% agreement, "
                f"average difference {avg_diff:.2f}"
            )


if __name__ == "__main__":
    main()
