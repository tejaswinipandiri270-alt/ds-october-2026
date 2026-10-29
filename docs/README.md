# Course documentation

Interactive reference pages (HTML) and notebooks for the **Data Science & Agentic AI Programme**, organised by week. More is added as the course goes on.

**Start here:** [index.html](index.html) is the landing page, with a searchable topic tracker.

> **To view the pages:** GitHub shows HTML files as source code. Clone or download the repo, then open `docs/index.html` in your browser. Each page works on its own offline, with light and dark modes.

**Key:** ✅ covered · ◐ partly covered · ⬜ not covered yet

---

## Week 0 · Onboarding: SDLC, Agile, Git, uv & EDA
*Wed 30 Sep – Fri 2 Oct*

| | Topic | Where |
|---|---|---|
| ✅ | SDLC: requirements, prototyping, PoC, development, testing, release (MVP), monitoring | [SDLC, Waterfall & Agile](week0/sdlc-agile-waterfall.html) |
| ✅ | Waterfall vs Agile | [SDLC, Waterfall & Agile](week0/sdlc-agile-waterfall.html) |
| ✅ | Testing types: unit, integration, smoke, regression, end-to-end, UAT | [SDLC, Waterfall & Agile](week0/sdlc-agile-waterfall.html) |
| ✅ | Scrum: roles, events, artefacts; how this programme runs as sprints | [Agile, Scrum & tickets](week0/agile-scrum-tickets.html) |
| ✅ | Writing tickets: user stories, acceptance criteria, Definition of Done, story points, WIP limits | [Agile, Scrum & tickets](week0/agile-scrum-tickets.html) · [Week 2 brief](../week2/README.md) |
| ✅ | Git essentials: fork, clone, branch, status, add, commit, push, pull | [Git & GitHub](week0/git-github.html) |
| ✅ | Merge vs rebase, conflicts, pull requests, keeping a fork in sync | [Git & GitHub](week0/git-github.html) |
| ✅ | Python environments with uv (init, venv, add, run, sync); VS Code, Jupyter, Colab | [Python, uv & Jupyter](week0/python-uv-jupyter.html) |
| ✅ | Exploratory data analysis: first look, distributions, relationships | [EDA & preprocessing](week0/eda-preprocessing.html) · [Titanic notebook](../week0/titanic_data_exploration.ipynb) |
| ✅ | Missing data, duplicates and outliers (IQR) | [EDA & preprocessing](week0/eda-preprocessing.html) · [Titanic notebook](../week0/titanic_data_exploration.ipynb) |
| ✅ | Imputation (mean / median / mode), encoding (label / one-hot), scaling (min-max / standard) | [EDA & preprocessing](week0/eda-preprocessing.html) · [Titanic notebook](../week0/titanic_data_exploration.ipynb) |

## Week 1 · Traditional Machine Learning
*Mon 5 – Fri 9 Oct*

| | Topic | Where |
|---|---|---|
| ✅ | Basic ML concepts: types of ML, features and labels, the ML workflow | [ML fundamentals & regression](week1/ml-fundamentals-regression.html) |
| ✅ | Train / validation / test splitting, stratification, data leakage | [ML fundamentals & regression](week1/ml-fundamentals-regression.html) |
| ✅ | Linear and multiple regression | [ML fundamentals & regression](week1/ml-fundamentals-regression.html) |
| ✅ | Regression metrics: MAE, MSE, RMSE, R² | [ML fundamentals & regression](week1/ml-fundamentals-regression.html) |
| ✅ | Bias–variance, overfitting vs underfitting (causes and fixes) | [ML fundamentals](week1/ml-fundamentals-regression.html) · [Classification guide](week1/classification-guide.html) |
| ✅ | Regularisation: Ridge (L2) and Lasso (L1) | [ML fundamentals & regression](week1/ml-fundamentals-regression.html) |
| ✅ | Logistic regression, naive Bayes, SVM | [Classification guide](week1/classification-guide.html) |
| ◐ | K-Nearest Neighbours (KNN): mentioned, no dedicated section yet | [ML fundamentals & regression](week1/ml-fundamentals-regression.html) |
| ✅ | Decision trees, Random Forest, Extra Trees | [Classification guide](week1/classification-guide.html) |
| ✅ | Boosting: AdaBoost, Gradient Boosting, XGBoost, LightGBM, CatBoost | [Classification guide](week1/classification-guide.html) |
| ✅ | Classification metrics, why accuracy misleads, ROC-AUC, PR-AUC | [Classification guide](week1/classification-guide.html) · [Imbalanced notebook](https://github.com/samuelts96/ds-october-2026-week1/blob/main/materials/imbalanced_classification.ipynb) |
| ✅ | Imbalanced data: SMOTE, undersampling, choosing a threshold | [Imbalanced notebook](https://github.com/samuelts96/ds-october-2026-week1/blob/main/materials/imbalanced_classification.ipynb) |
| ✅ | Cross-validation and hyperparameter tuning (grid & random search) | [Classification guide](week1/classification-guide.html) · [Tuning notebook](https://github.com/samuelts96/ds-october-2026-week1/blob/main/materials/tuning_roc_kmeans.ipynb) |
| ✅ | Unsupervised learning: K-Means, elbow method, silhouette score | [Unsupervised learning & K-Means](week1/unsupervised-kmeans.html) · [Tuning notebook](https://github.com/samuelts96/ds-october-2026-week1/blob/main/materials/tuning_roc_kmeans.ipynb) |
| ◐ | Other clustering: DBSCAN, hierarchical, Gaussian mixtures (overview only) | [Unsupervised learning & K-Means](week1/unsupervised-kmeans.html) |

## Week 2 · Deep Learning, MLflow, MLOps & FastAPI (theory)
*Mon 12 – Fri 16 Oct*

| | Topic | Where |
|---|---|---|
| ✅ | Neurons, activation functions, MLPs and deep networks, the forward pass | [Deep learning foundations](week2/deep-learning-foundations.html) |
| ✅ | Loss functions, backpropagation, gradient descent | [Deep learning foundations](week2/deep-learning-foundations.html) |
| ✅ | Optimisers (SGD, momentum, RMSprop, Adam) and the learning rate | [Deep learning foundations](week2/deep-learning-foundations.html) |
| ✅ | Regularisation in DL: dropout, early stopping, batch normalisation | [Deep learning foundations](week2/deep-learning-foundations.html) |
| ✅ | CNNs: convolution, pooling, transfer learning | [Neural network architectures](week2/neural-network-architectures.html) |
| ✅ | Object detection & segmentation with pretrained YOLO | [Neural network architectures](week2/neural-network-architectures.html) |
| ✅ | RNNs, LSTMs and GRUs | [Neural network architectures](week2/neural-network-architectures.html) |
| ✅ | Experiment tracking with MLflow: runs, params, metrics, artifacts, autolog | [MLflow & experiment tracking](week2/mlflow-experiment-tracking.html) |
| ✅ | MLflow: tagging experiments and runs, searching and comparing runs | [MLflow & the MLOps pipeline](week2/mlflow-mlops-pipeline.html) |
| ✅ | Model registry: versions, aliases, champion vs challenger | [MLflow & the MLOps pipeline](week2/mlflow-mlops-pipeline.html) · [MLflow & experiment tracking](week2/mlflow-experiment-tracking.html) |
| ✅ | MLOps theory: training, evaluation, promotion, monitoring, retraining, rollback | [MLflow & the MLOps pipeline](week2/mlflow-mlops-pipeline.html) |
| ✅ | Monitoring: data drift and model drift (PSI, KS test) | [MLflow & the MLOps pipeline](week2/mlflow-mlops-pipeline.html) |
| ✅ | FastAPI theory: URLs, IPv4, localhost / 127.0.0.1 / 0.0.0.0, ports, routes and endpoints | [FastAPI & serving models](week2/fastapi-serving.html) |
| ✅ | HTTP methods and status codes: 200, 4xx (400, 404, 405, 422), 5xx (500, 503) | [FastAPI & serving models](week2/fastapi-serving.html) |

## Week 3 · Time Series & MLOps
*Mon 19 – Fri 23 Oct · Tech Eval 1 on Thu–Fri (ML and DL)*

| | Topic | Where |
|---|---|---|
| ◐ | Day 1 · FastAPI for ML deployment: Pydantic validation, Swagger UI, `/health`, `/predict`, `/model-info` | [FastAPI & serving models](week2/fastapi-serving.html) (theory and serving; no `/model-info` yet) |
| ⬜ | Serving a scikit-learn model loaded with Joblib; feature order and preprocessing | |
| ◐ | API testing with pytest and TestClient | [FastAPI & serving models](week2/fastapi-serving.html) |
| ⬜ | Day 2 · Docker: Dockerfile, images vs containers, port mapping, volumes, networking | |
| ⬜ | Docker Compose: services, networks, `depends_on`, up / down / logs | |
| ⬜ | Time series: trend, seasonality, stationarity, forecasting | |
| ⬜ | Streamlit apps | |

## Week 4 · NLP, Transformers & Large Language Models
*Mon 26 – Fri 30 Oct* · setup: [week4/README.md](../week4/README.md) · reading: [NLP basics & embeddings](week4/nlp-basics.html), [Prompt engineering](week4/prompt-engineering.html) · project: [week4/PROJECTS.md](../week4/PROJECTS.md)

| | Topic | Where |
|---|---|---|
| ✅ | NLP basics: tokenisation, normalisation, stop words (keeping negations), stemming vs lemmatisation, n-grams | [NLP basics & embeddings](week4/nlp-basics.html) · [NLP basics notebook](../week4/01_nlp_vectorization_restaurant_reviews.ipynb) |
| ✅ | Vectorisation: Bag of Words, TF-IDF, Word2Vec (CBOW vs skip-gram), GloVe | [NLP basics & embeddings](week4/nlp-basics.html) · [NLP basics notebook](../week4/01_nlp_vectorization_restaurant_reviews.ipynb) |
| ✅ | Vectors vs embeddings, with model examples | [NLP basics & embeddings](week4/nlp-basics.html) · [NLP basics notebook](../week4/01_nlp_vectorization_restaurant_reviews.ipynb) |
| ✅ | Attention, transformers and BERT (contextual embeddings) | [NLP basics & embeddings](week4/nlp-basics.html) · [NLP basics notebook](../week4/01_nlp_vectorization_restaurant_reviews.ipynb) |
| ✅ | From embeddings to LLMs: how LLMs are trained, in brief | [NLP basics & embeddings](week4/nlp-basics.html) · [NLP basics notebook](../week4/01_nlp_vectorization_restaurant_reviews.ipynb) |
| ✅ | Prompt engineering: zero-shot, few-shot, structured output, chain of thought, tree of thought | [Prompt engineering](week4/prompt-engineering.html) · [Prompt engineering notebook](../week4/02_prompt_engineering_simple.ipynb) |
| ✅ | Guardrails and LLM-as-a-judge | [Prompt engineering](week4/prompt-engineering.html) · [Prompt engineering notebook](../week4/02_prompt_engineering_simple.ipynb) |
| ✅ | RAG basics: semantic search, grounded answers with citations | [NLP basics & embeddings](week4/nlp-basics.html) · [Prompt engineering](week4/prompt-engineering.html) · [NLP basics notebook](../week4/01_nlp_vectorization_restaurant_reviews.ipynb) |
| ✅ | Calling Azure OpenAI; running and serving an LLM locally (Ollama, FastAPI) | [Prompt engineering](week4/prompt-engineering.html) · [Prompt engineering notebook](../week4/02_prompt_engineering_simple.ipynb) |
| ✅ | Structured outputs validated with Pydantic (with a retry) | [Prompt engineering](week4/prompt-engineering.html) · [Prompt engineering notebook](../week4/02_prompt_engineering_simple.ipynb) |
| ✅ | Comparing prompting strategies: field-level accuracy on a labelled set | [Prompt engineering](week4/prompt-engineering.html) · [Prompt engineering notebook](../week4/02_prompt_engineering_simple.ipynb) |

## Coming up (not documented yet)

| Week | | Topic |
|---|---|---|
| 5 · Embeddings & RAG | ⬜ | Chunking, vector databases, hybrid retrieval, re-ranking, RAG evaluation |
| 6 · Fine-tuning & guardrails | ⬜ | LoRA / QLoRA, instruction tuning, RLHF / DPO, LLM evaluation, guardrails |
| 7 · Single-agent systems | ⬜ | Agent loop, tool calling, memory, planning, LangGraph, MCP |
| 8 · Multi-agent & capstone | ⬜ | Orchestration patterns, observability, deployment, capstone |

---

## Adding a new page

1. Put the HTML file in `docs/weekN/`. Copy the structure and `<style>` block of an existing page so the look stays consistent.
2. Add it to the `DOCS` and `WEEKS` lists in [index.html](index.html), and update the tables above (change ⬜ to ✅).
