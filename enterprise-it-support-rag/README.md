# Enterprise IT Support RAG Assistant

Local-first RAG starter with PDF/DOCX/TXT ingestion, chunking, Sentence Transformers embeddings, persistent Chroma, BM25 + dense hybrid retrieval with reciprocal-rank fusion, local Ollama generation, FastAPI, Streamlit, tests and evaluation.

> Production-oriented starter, not a certified production deployment. The included IT policies are fictional training examples. Complete security, privacy, authorization, retention, monitoring and load-testing reviews before real employee use.

## Requirements
Windows 10/11, Python 3.11/3.12 recommended, VS Code, Ollama. First embedding-model run downloads `sentence-transformers/all-MiniLM-L6-v2`.

## Setup (PowerShell from this project root)
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
ollama pull qwen2.5:3b
```
If `py -3.12` is unavailable, create the venv using a known Python executable:
```powershell
& "C:\Path\To\python.exe" -m venv .venv
.\.venv\Scripts\Activate.ps1
```
If activation is blocked:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run
1. Start Ollama (if not already running): `ollama serve`
2. Ingest sample docs: `python -m backend.cli ingest`
3. Start API: `uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000`
4. In another terminal: `streamlit run frontend/app.py`
5. API docs: http://127.0.0.1:8000/docs

Run tests: `python -m pytest -q`
Retrieval evaluation after ingestion: `python -m evaluation.evaluate_retrieval`

## API
`GET /health`, `POST /ingest`, `POST /upload`, `POST /retrieve`, `POST /chat`, `POST /feedback`.
Set `API_KEY` in `.env` to protect ingestion/upload endpoints; provide `X-API-Key`. Empty API_KEY disables this protection for local development.

## Layout
- `backend/rag`: loaders, chunking, embeddings, Chroma, BM25/hybrid retrieval, pipeline
- `backend/services`: Ollama generation
- `backend/api`: FastAPI routes
- `frontend`: Streamlit UI
- `data/documents`: fictional sample policies
- `evaluation`: sample questions and Hit@K/MRR evaluation
- `tests`: unit tests
- `.vscode/settings.json`: project venv and Pylance settings

## Security checklist before deployment
Use approved documents only; never upload passwords/tokens. Document-level access control is not implemented, so do not mix different permission classes. Configure strong API key, TLS/reverse proxy, restricted CORS, backups, retention, monitoring, audit controls and authentication/authorization. Treat retrieved documents as untrusted. Do not expose this local development API publicly.

## Docker (optional)
`docker compose up --build`. Ollama is expected on the Windows host at port 11434. Local Python + local Ollama is the simplest first run.

## Troubleshooting
- Pylance: select `.venv\Scripts\python.exe` and reload VS Code.
- Ollama connection refused: start Ollama; check `ollama list`.
- Empty knowledge base: run `python -m backend.cli ingest`.
- Run all commands from the project root.
