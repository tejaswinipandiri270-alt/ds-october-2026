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

## Week 2 · Deep Learning Foundations & Intro to MLflow
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
| ✅ | Model registry, versions, champion / challenger aliases (preview) | [MLflow & experiment tracking](week2/mlflow-experiment-tracking.html) |

## Coming up (not documented yet)

| Week | | Topic |
|---|---|---|
| 3 · Time Series & MLOps | ⬜ | Time series: trend, seasonality, stationarity, forecasting, chronological validation |
| | ◐ | MLflow in an MLOps pipeline: registry and promotion (basics in the MLflow page) |
| | ⬜ | FastAPI: routes, endpoints (`/health`, `/v1/process`), validation, status codes 200 / 400 / 422 / 500 |
| | ◐ | MLOps pipeline: training, challenger vs champion, promotion (basics in the MLflow page) |
| | ⬜ | Monitoring: data drift and model drift |
| | ⬜ | Streamlit apps; moving from notebooks to Python scripts |
| 4 · NLP, Transformers & LLMs | ⬜ | Text preparation, embeddings, attention, transformers, BERT / GPT / T5, Hugging Face, LLM APIs, prompting |
| 5 · Embeddings & RAG | ⬜ | Chunking, vector databases, hybrid retrieval, re-ranking, RAG evaluation |
| 6 · Fine-tuning & guardrails | ⬜ | LoRA / QLoRA, instruction tuning, RLHF / DPO, LLM evaluation, guardrails |
| 7 · Single-agent systems | ⬜ | Agent loop, tool calling, memory, planning, LangGraph, MCP |
| 8 · Multi-agent & capstone | ⬜ | Orchestration patterns, observability, deployment, capstone |

---

## Adding a new page

1. Put the HTML file in `docs/weekN/`. Copy the structure and `<style>` block of an existing page so the look stays consistent.
2. Add it to the `DOCS` and `WEEKS` lists in [index.html](index.html), and update the tables above (change ⬜ to ✅).
