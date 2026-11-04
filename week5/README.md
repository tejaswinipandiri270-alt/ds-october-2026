# Week 5 · Embeddings and Retrieval-Augmented Generation

**Mon 2 – Fri 6 Nov 2026**

| Notebook | What it covers |
|---|---|
| [01_rag_faiss_chroma.ipynb](01_rag_faiss_chroma.ipynb) | RAG step by step on a small restaurant handbook: chunking (paragraphs, fixed size with overlap) · embeddings with `all-MiniLM-L6-v2` · brute-force search · **FAISS** (flat index, save and load, approximate indexes) · **Chroma** (collections, metadata filters, upsert) · FAISS vs Chroma · a similarity threshold for "I don't know" · answering with Azure OpenAI and citing sources · splitting multi-topic questions · evaluating retrieval with hit rate and MRR |

**Reading:** [RAG with FAISS and Chroma](../docs/week5/rag-faiss-chroma.html) explains every step of the notebook.

## Setup

```bash
uv add faiss-cpu chromadb sentence-transformers openai python-dotenv pandas numpy jupyter
```

Steps 1–6 and 8 run on your laptop with no API key (the embedding model downloads once, about 90 MB).
Step 7 calls **Azure OpenAI**: copy [`.env.example`](.env.example) to `.env` next to the notebook and fill in the values the trainer shares.
`.env` is in `.gitignore`: **never commit it**.

The notebook is saved with its outputs, except the cells starting with **# 🤖 calls the LLM**: run those yourself.
It writes `restaurant.faiss` and `restaurant_chunks.json` when you run it (Step 4.3); you don't need to commit them.
