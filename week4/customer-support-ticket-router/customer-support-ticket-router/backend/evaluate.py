"""Run a field-level accuracy comparison over the hand-labelled synthetic examples.
Usage from the project root: python -m backend.evaluate
"""
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from backend.llm_service import classify_email
from backend.prompts import PROMPT_FUNCTIONS

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
DATA_PATH = ROOT / "data" / "labelled_examples.json"
FIELDS = ["category", "priority", "product", "customer_wants"]

def norm(value):
    return str(value).strip().casefold()

def main():
    examples = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    if len(examples) < 20:
        raise SystemExit(f"Need at least 20 labelled examples; found {len(examples)}.")
    scores = {}
    for technique in PROMPT_FUNCTIONS:
        correct = {field: 0 for field in FIELDS}
        print(f"Running technique: {technique}")
        for i, row in enumerate(examples, start=1):
            predicted = classify_email(row["input"], technique=technique).model_dump()
            expected = row["expected"]
            for field in FIELDS:
                # Product names are compared case-insensitively after trimming whitespace.
                if norm(predicted[field]) == norm(expected[field]):
                    correct[field] += 1
            print(f"  {i}/{len(examples)} complete", end="\r", flush=True)
        scores[technique] = {
            field: round(100 * correct[field] / len(examples), 1)
            for field in FIELDS
        }
        print()
    print("\nFIELD-LEVEL ACCURACY (%)")
    print("| Technique | " + " | ".join(FIELDS) + " |")
    print("|---|" + "|".join(["---:"] * len(FIELDS)) + "|")
    for technique, row in scores.items():
        print("| " + technique + " | " + " | ".join(str(row[f]) for f in FIELDS) + " |")
    out = ROOT / "data" / "accuracy_results.json"
    out.write_text(json.dumps({"n_examples": len(examples), "scores_percent": scores}, indent=2), encoding="utf-8")
    print(f"\nSaved raw accuracy results to {out}")
    print("Review these measured results before choosing the production prompt in backend/main.py.")

if __name__ == "__main__":
    main()
