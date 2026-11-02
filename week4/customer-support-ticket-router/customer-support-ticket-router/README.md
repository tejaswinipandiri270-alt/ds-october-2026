# Customer Support Ticket Router (LLM)

A Week 4 NLP/LLM project. It accepts a support email, extracts structured ticket fields, drafts a safe first reply, and asks an LLM judge to score the reply.

## Features mapped to the project brief

1. **Prompt engineering:** separate zero-shot, few-shot, and role-based prompt functions in `backend/prompts.py`.
2. **Structured output:** Pydantic models in `backend/schemas.py`; classification output gets one retry if JSON/Pydantic validation fails.
3. **Accuracy comparison:** 20+ hand-labelled synthetic examples in `data/labelled_examples.json`; run all three techniques and report field-level accuracy.
4. **LLM as judge:** 1–5 scores for answering the question, tone, and policy compliance, with a reason; judge result is Pydantic-validated.
5. **FastAPI:** `GET /health` and `POST /classify`; request/response schemas and error handling.
6. **Streamlit:** calls FastAPI only and displays the classification, drafted reply, and judge scores.
7. **Docker:** separate backend/frontend Dockerfiles and Compose setup.
8. **Secrets:** `.env` is ignored by Git; `.env.example` contains placeholders.

No MLflow or model training is required for this project.

## 1. Requirements

- Python 3.12 recommended for local development.
- An Azure OpenAI resource and a deployed chat model.
- Docker Desktop if you want to use Docker Compose.

## 2. Configure Azure OpenAI

From the project root, copy `.env.example` to `.env` and enter your real Azure deployment settings:

```text
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-secret-key
AZURE_OPENAI_API_VERSION=your-supported-api-version
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
```

Use the API version and deployment name supplied by your Azure setup. The deployment name is not necessarily the same as the base model name.

**Never commit `.env` or paste real customer data/API keys into GitHub.** The app is intended for synthetic or anonymised examples.

## 3. Run locally in VS Code

Open the `customer-support-ticket-router` folder in VS Code. In the terminal, run these commands from the project root.

### Windows PowerShell: backend

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
pip install -r frontend\requirements.txt
Copy-Item .env.example .env
```

Edit `.env` before making LLM requests. If PowerShell blocks activation, use the VS Code terminal settings or run the environment's Python directly: `.\.venv\Scripts\python.exe`.

Start the backend in terminal 1:

```powershell
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Check `http://127.0.0.1:8000/health`. Interactive API docs are at `http://127.0.0.1:8000/docs`.

Start Streamlit in terminal 2, with the same virtual environment active:

```powershell
python -m streamlit run frontend/app.py
```

Open `http://localhost:8501`.

## 4. Compare prompting techniques

From the project root with `.env` configured:

```powershell
python -m backend.evaluate
```

The script evaluates all labelled rows using zero-shot, few-shot, and role-based prompting, prints a field-level accuracy table, and writes `data/accuracy_results.json`.

This sends multiple requests to Azure OpenAI and may incur usage costs. Run it when ready, not repeatedly without need.

### Report your real results

Copy the actual printed scores into your report/README. Do not claim an accuracy value before running the evaluation. Choose the production prompt based on the results and consistency. The API currently defaults to `few_shot` in `backend/main.py`; change that after reviewing your results if another technique performs better.

## 5. LLM judge calibration (10 examples)

For 10 generated replies, score each criterion yourself using the same rubric as the judge. Copy the judge scores from the app/API response. Create `data/judge_calibration.csv` with these columns:

```csv
example_id,human_question_answering_score,human_tone_score,human_policy_compliance_score,judge_question_answering_score,judge_tone_score,judge_policy_compliance_score
1,4,5,5,4,5,5
```

The single row above is an illustrative format only; replace it with your own real ratings and include at least 10 rows. Then run:

```powershell
python -m backend.calibrate_judge
```

The script reports exact agreement across the paired criterion ratings. In your README, explain disagreements and note that LLM judge scores are not ground truth. (Do not report the illustrative values as results.)

## 6. Run with Docker Compose

1. Ensure `.env` exists and has valid Azure settings.
2. From the project root run:

```powershell
docker compose up --build
```

3. Open Streamlit at `http://localhost:8501`.
4. Check the backend at `http://localhost:8000/health`.
5. Stop the services with `Ctrl+C`, then `docker compose down`.

Compose connects Streamlit to FastAPI using `http://backend:8000` on the internal Docker network. `localhost` inside a container would refer to that same container, not the other service.

## API

### `GET /health`

Returns service status without calling Azure OpenAI.

### `POST /classify`

Request:

```json
{"email": "I was charged twice for my Premium plan. Please review the extra charge."}
```

Response contains:
- `classification`: category, priority, product, customer_wants
- `draft_reply`: first reply for a human to review
- `judge`: three scores (1–5) and a reason
- `prompt_technique`: technique used

HTTP 422 is returned for request schema errors. HTTP 400 is used for application-level invalid input. HTTP 503 is used when the model service/configuration or LLM processing is unavailable.

## Dataset and labelling rules

The included examples are synthetic and manually labelled. Keep the same policy definitions across all techniques. `product` accuracy uses exact case-insensitive matching after trimming whitespace; this is intentionally strict. If you want to allow aliases such as “mobile app” vs “app”, define a documented normalisation rule before evaluating and apply it consistently.

## Suggested report sections

1. Problem and objective
2. Dataset and labelling rules
3. Three prompting techniques
4. Pydantic validation and retry
5. Field-level accuracy comparison table
6. Selected prompt technique and justification
7. Reply-generation rubric
8. LLM judge calibration: 10 examples, agreement percentage, disagreements
9. FastAPI/Streamlit/Docker architecture
10. Limitations, safety and future improvements

## Limitations and safety

- The judge is another LLM call and can be wrong or inconsistent.
- Draft replies must be reviewed by a human before sending.
- Never promise refunds, account changes, or delivery dates without authorised policy/data.
- Do not enter real personal, payment, health, or confidential data.
- Azure model deployment/API versions depend on your organisation's Azure configuration.
