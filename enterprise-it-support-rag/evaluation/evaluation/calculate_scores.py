import json
from pathlib import Path

file_path = Path("final_answer_evaluation_results.json")

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

print("Total tests:", len(data))

metrics = [
    "faithfulness",
    "answer_relevance",
    "context_precision",
    "context_recall"
]

for metric in metrics:
    average = sum(
        item["scores"][metric] for item in data
    ) / len(data)

    print(f"{metric}: {average:.2f}/5")