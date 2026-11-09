import argparse
from backend.rag.pipeline import RAGPipeline

def main():
    parser = argparse.ArgumentParser(description="IT Support RAG CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    ingest = sub.add_parser("ingest")
    ingest.add_argument("--directory", default=None)
    args = parser.parse_args()
    if args.command == "ingest":
        print(RAGPipeline().ingest_directory(args.directory))

if __name__ == "__main__":
    main()
