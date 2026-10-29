# Week 4 · NLP, Transformers & Large Language Models

**Mon 26 – Fri 30 Oct 2026**

| Notebook | What it covers |
|---|---|
| [01_nlp_vectorization_restaurant_reviews.ipynb](01_nlp_vectorization_restaurant_reviews.ipynb) | NLP basics (tokenisation, normalisation, stop words and the negation trap, stemming vs lemmatisation, n-grams) · Bag of Words, TF-IDF · Word2Vec (CBOW vs skip-gram), GloVe · vectors vs embeddings with model examples · attention, transformers and BERT (contextual embeddings) · sentence embeddings and semantic search · how LLMs are trained, in brief |
| [02_prompt_engineering_simple.ipynb](02_prompt_engineering_simple.ipynb) | Connect to Azure OpenAI and say hello · zero-shot, few-shot, role prompting, chain of thought · structured JSON output · validating it with Pydantic · comparing the accuracy of prompting strategies on a labelled set · LLM as a judge, and checking the judge against gold labels |

Notebook 1 uses 1,000 restaurant reviews labelled liked / not liked (loaded from the web, nothing to download by hand). Notebook 2 uses a few short reviews written into the notebook.

**Project:** each person builds one LLM app (prompt engineering, Pydantic, LLM as a judge, FastAPI, Streamlit, Docker). See **[PROJECTS.md](PROJECTS.md)**.

**Reading:** [NLP basics](../docs/week4/nlp-basics.html) and [Prompt engineering](../docs/week4/prompt-engineering.html) in the docs.

## Setup

```bash
uv add pandas numpy scikit-learn matplotlib nltk gensim sentence-transformers transformers torch openai python-dotenv pydantic jupyter
```

**Notebook 2 uses Azure OpenAI** (the v1 API, so no `api-version` is needed). Copy [`.env.example`](.env.example) to `.env` in the same folder as the notebooks and fill in the values the trainer shares:

```bash
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com/
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_DEPLOYMENT=<your-chat-deployment-name>
```

`.env` is in `.gitignore`: **never commit it, and never paste keys into a notebook**.


Notebook 1 is saved with all its outputs. In Notebook 2, the cells starting with **# 🤖 calls the LLM** are saved without outputs: run them yourself, because answers vary between models and runs.
