# Week 3 · Deploy your model locally: MLflow + FastAPI + Streamlit

**Presented on Tuesday 27 October 2026**

Take **your Week 2 project** (the same dataset and the deep learning models you tracked in MLflow) and turn it into a small working application that runs on your laptop:

```
 ┌──────────────────────┐   HTTP POST /predict    ┌──────────────────────┐   loads models:/<name>@champion   ┌──────────────────────┐
 │  Streamlit frontend  │ ──────────────────────▶ │   FastAPI backend    │ ────────────────────────────────▶ │    MLflow server     │
 │  localhost:8501      │ ◀────────────────────── │   localhost:8000     │                                   │    localhost:5000    │
 │  form → prediction   │     JSON response       │  /health /predict    │                                   │ runs · registry ·    │
 └──────────────────────┘                         │  /model-info         │                                   │ champion alias       │
                                                  └──────────────────────┘                                   └──────────────────────┘
```

| Contents |
|---|
| [1. What you're building](#1-what-youre-building) |
| [2. MLflow server](#2-mlflow-server) |
| [3. FastAPI backend](#3-fastapi-backend) |
| [4. Streamlit frontend](#4-streamlit-frontend) |
| [5. Running it locally](#5-running-it-locally) |
| [6. Stretch: Docker Compose](#6-stretch-docker-compose) |
| [7. Push to GitHub](#7-push-to-github) |
| [8. Tuesday presentation](#8-tuesday-presentation) |

Reference pages: [MLflow & the MLOps pipeline](../docs/week2/mlflow-mlops-pipeline.html) · [FastAPI & serving models](../docs/week2/fastapi-serving.html) · [MLflow & experiment tracking](../docs/week2/mlflow-experiment-tracking.html)

---

## 1. What you're building

| Component | Job | Port |
|---|---|---|
| **MLflow server** | Stores your experiments, runs and the **model registry**. Your best model is registered with the alias **`champion`** | `5000` |
| **FastAPI backend** | Loads the champion model **once at startup** from the MLflow server and serves predictions | `8000` |
| **Streamlit frontend** | A simple web page where a user fills in the inputs, clicks Predict and sees the result | `8501` |

**Carry forward from Week 2:** your dataset (Adult Census Income, California Housing or Fashion-MNIST), your preprocessing, and your experiments. You can re-log them to the new MLflow server (see section 2).

## 2. MLflow server

Last week MLflow wrote to a local file. This week you run it as a **server**, the way a team would share one.

```bash
uv run mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --artifacts-destination ./mlartifacts \
  --host 127.0.0.1 --port 5000
```

Open http://127.0.0.1:5000. Then, in your training script, point MLflow at the server **before** logging anything:

```python
import mlflow
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("w3-<your-project>")
```

**What must be in MLflow by Tuesday:**
- At least **3 runs** (your Week 2 models, or improved ones), **tagged** (e.g. `model_family`, `algorithm`, `stage`) and compared
- The best model **registered** (e.g. `adult-income-classifier`) with the alias **`champion`**
- (Recommended) a second version with the alias **`challenger`**, and your rule for promoting it

```python
from mlflow import MlflowClient
mv = mlflow.register_model(model_info.model_uri, "adult-income-classifier")
MlflowClient().set_registered_model_alias("adult-income-classifier", "champion", mv.version)
```

## 3. FastAPI backend

A `main.py` with at least these endpoints:

| Method | Route | Returns |
|---|---|---|
| `GET` | `/health` | `{"status": "ok", "model_loaded": true, "model_version": "1"}`, or **503** if the model didn't load |
| `POST` | `/predict` | The prediction (class label and probability, or a number for regression) for one input |
| `GET` | `/model-info` | Model name, version, alias, metrics, and the feature names it expects, in order |

Requirements:
- **Load the model once** at startup (FastAPI `lifespan`) from `models:/<name>@champion`. **Never** load it per request.
- A **Pydantic** request model with types and `Field` constraints (e.g. `age: int = Field(ge=17, le=100)`), so bad input gets a **422**.
- Use the **same preprocessing** as in training, with features in the **same order**.
- The right **status codes**: 200 success, 422 invalid input, 400 for business-rule errors, 503 when the model isn't loaded, 500 never leaking a stack trace.
- Swagger docs at http://127.0.0.1:8000/docs work.

```bash
MLFLOW_TRACKING_URI=http://127.0.0.1:5000 uv run uvicorn main:app --reload --port 8000
```

## 4. Streamlit frontend

An `app.py` that:
- Shows a form with your model's inputs (number inputs, select boxes; for images, `st.file_uploader`)
- On **Predict**, calls `POST http://127.0.0.1:8000/predict` with `requests` and shows the result clearly
- Shows the model name and version (from `/model-info`)
- Shows a friendly message when the API is down or returns 422 / 500, instead of a crash

```python
import requests, streamlit as st

API_URL = "http://127.0.0.1:8000"
st.title("Adult income predictor")
age = st.number_input("Age", 17, 100, 35)
# ... more inputs ...
if st.button("Predict"):
    r = requests.post(f"{API_URL}/predict", json={"age": age}, timeout=10)
    if r.status_code == 200:
        st.success(r.json())
    else:
        st.error(f"API returned {r.status_code}: {r.json().get('detail')}")
```

```bash
uv run streamlit run app.py      # opens http://localhost:8501
```

## 5. Running it locally

Three terminals, in this order:

```bash
# 1. MLflow server
uv run mlflow server --backend-store-uri sqlite:///mlflow.db --artifacts-destination ./mlartifacts --host 127.0.0.1 --port 5000
# 2. FastAPI (after the champion is registered)
MLFLOW_TRACKING_URI=http://127.0.0.1:5000 uv run uvicorn main:app --reload --port 8000
# 3. Streamlit
uv run streamlit run app.py
```

Check: http://127.0.0.1:5000 (MLflow) · http://127.0.0.1:8000/health and /docs (API) · http://localhost:8501 (app).

**Common problems**
- **"Address already in use"**: something is already on that port. Stop it (`lsof -i :8000`), or use another port and update the URLs.
- **The API can't find the model**: is the MLflow server running, did you set `MLFLOW_TRACKING_URI`, and does the alias name match exactly?
- **Wrong or odd predictions**: check the feature order and that preprocessing (scaling, encoding) is identical to training.

## 6. Stretch: Docker Compose

Using Wednesday's material, run all three as services with one `compose.yaml` and `docker compose up`:
- Each service binds to `0.0.0.0` inside its container, and the ports are published (`5000:5000`, `8000:8000`, `8501:8501`).
- Services talk to each other **by service name**, not `localhost`: the API uses `MLFLOW_TRACKING_URI=http://mlflow:5000`, and Streamlit uses `API_URL=http://api:8000`.
- ⚠️ **MLflow 3 blocks unknown host names.** A request to `mlflow:5000` gets **`403 Invalid Host header`** unless the server allows it. Start the MLflow service with e.g. `--host 0.0.0.0 --port 5000 --allowed-hosts "mlflow,mlflow:5000,localhost,localhost:5000,127.0.0.1,127.0.0.1:5000"`.
- Use a volume for `mlflow.db` and `mlartifacts/` so your runs survive a restart.

## 7. Push to GitHub

On your fork of this repo, branch `week3/<your-name>`:

```
week3/<your-name>/
├── README.md          # architecture, how to run it (the 3 commands), screenshots
├── train.py           # trains, logs, tags and registers the champion
├── main.py            # FastAPI backend
├── app.py             # Streamlit frontend
├── pyproject.toml     # or requirements.txt
├── compose.yaml       # stretch
└── screenshots/       # MLflow runs + registry, Swagger /docs, Streamlit app
```

Add `mlflow.db`, `mlruns/`, `mlartifacts/` and `.venv/` to `.gitignore`. Post the branch link on your Trello card.

## 8. Tuesday presentation

**Tuesday 27 October · 10 minutes per person or team**

| Part | Time | Content |
|---|---|---|
| **1. Recap** | 1 min | The business problem and dataset from Week 2 |
| **2. Architecture** | 2 min | Your diagram: Streamlit → FastAPI → MLflow, the ports, and what each part does |
| **3. MLflow** | 2 min | Runs and tags, the comparison, the registered model and the **champion** alias (plus challenger and promotion rule if you have them) |
| **4. Live demo** | 3 min | Streamlit prediction end to end; `/health` and `/docs`; a **bad input** returning 422 and how the UI handles it |
| **5. Lessons** | 2 min | What broke and how you fixed it; what you'd add next (Docker Compose, monitoring, drift checks) |

Have screenshots ready in case the live demo fails.

## Checklist

- [ ] MLflow server running; 3+ tagged runs; best model registered as `champion`
- [ ] FastAPI: `/health`, `/predict`, `/model-info`, Pydantic validation, correct status codes, model loaded once
- [ ] Streamlit app calling the API, handling errors gracefully
- [ ] All three running locally with the commands in your README
- [ ] Code and screenshots pushed to `week3/<your-name>`, link on your Trello card
- [ ] Presentation ready for Tuesday 27 October (10 minutes)
- [ ] Stretch: `docker compose up` runs all three
