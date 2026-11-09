import json
from pathlib import Path
from backend.rag.pipeline import RAGPipeline

def main():
    cases = json.loads(Path(__file__).with_name("questions.json").read_text(encoding="utf-8"))
    rag = RAGPipeline()
    hits, rr = 0, 0.0
    for case in cases:
        found = [x.get("metadata", {}).get("filename") for x in rag.retrieve(case["question"], 5)]
        expected = case["expected_source"]
        if expected in found:
            hits += 1
            rr += 1 / (found.index(expected) + 1)
        print(f"Q: {case['question']}\\nExpected: {expected}\\nRetrieved: {found}\\n")
    print(f"Hit@5: {hits/len(cases):.3f} | MRR@5: {rr/len(cases):.3f}")

if __name__ == "__main__":
    main()
