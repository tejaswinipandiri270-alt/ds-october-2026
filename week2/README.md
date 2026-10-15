# Week 2 · Deep learning + MLflow, run as a real sprint

**Mon 12 - Fri 16 Oct 2026** · Presented on **Tuesday 20 October**

This week **you run your own sprint**: you plan the work as tickets on the Trello board, build several deep learning models, track every experiment in **MLflow**, and push it all to GitHub.

Your **dataset link is on the "Week 2" card** in the Programme list on Trello.

| Contents |
|---|
| [1. The goal](#1-the-goal) |
| [2. Create your own cards (Agile tickets)](#2-create-your-own-cards-agile-tickets) |
| [3. The work](#3-the-work) |
| [4. Track experiments in MLflow](#4-track-experiments-in-mlflow) |
| [5. Push to GitHub](#5-push-to-github) |
| [6. Tuesday presentation](#6-tuesday-presentation) |

---

## 1. The goal

> Build **at least 3 deep learning models** for your dataset, **track every run in MLflow**, choose the best one with evidence, and **push it to GitHub**, all planned and tracked as **tickets on the board**.

The code can stay simple; the focus is on **experiment tracking and working the Agile way**.

---

## 2. Create your own cards (Agile tickets)

In industry, work is planned as **tickets** (Jira, Trello, Azure DevOps…). This week you write your own.

### Break the work into small tickets

**Don't** create one giant card called "Week 2". Create **one card per piece of work** that can be finished in about a day or less. For example:

| # | Ticket |
|---|---|
| 1 | Set up the project environment and MLflow |
| 2 | Load, explore and prepare the dataset |
| 3 | Train a baseline neural network (MLP) |
| 4 | Experiment: deeper network, dropout, batch normalisation |
| 5 | Experiment: optimisers and learning rates |
| 6 | Compare runs in MLflow and choose the best model |
| 7 | Push the code, README and MLflow screenshots to GitHub |
| 8 | Prepare Tuesday's presentation |

Put them in **Sprint To Do**, labelled **W2**.

### What every ticket needs

| Part | What to write | Example |
|---|---|---|
| **Title** | Short and action-first, starting with your name so the board can be filtered. Optionally an estimate in brackets | `W2 · Helena · Train baseline MLP [2]` |
| **Description** | The *why* and the context, often as a **user story**: *As a … I want … so that …* | *As a data scientist I want a simple baseline network so that I have a benchmark to beat.* |
| **Acceptance criteria** | **Testable** conditions that must all be true to call it done. Write them as a checklist on the card | ☐ 2 hidden layers, ReLU · ☐ trained on train, evaluated on validation · ☐ run logged in MLflow with params, metrics and loss curve · ☐ validation score noted in a comment |
| **Member** | Assign yourself | *(your avatar)* |
| **Label** | `W2` | |
| **Due date** | When you'll finish it | Thu 15 Oct |
| **Estimate** | The effort in **story points** (1, 2, 3, 5, 8: relative size, not hours) | `[2]` in the title |
| **Links** | Your GitHub branch or commit, MLflow screenshots | as a comment or attachment |
| **Comments** | Progress updates, blockers, decisions | *"Blocked: TensorFlow won't install on Python 3.13, switching to 3.12"* |

> **Acceptance criteria vs Definition of Done.** *Acceptance criteria* are specific to one ticket ("val loss logged per epoch"). The *Definition of Done* applies to **every** ticket:
> 1. Every acceptance criterion is ticked
> 2. The code is pushed to your branch on GitHub
> 3. The experiment is logged in MLflow
> 4. Notes or links are added as a comment
> 5. The card is moved to **Review**

### Good tickets are INVEST

**I**ndependent · **N**egotiable · **V**aluable · **E**stimable · **S**mall · **T**estable

If you can't write acceptance criteria for it, it's too vague. If it takes more than a day, split it.

### Work the board

- Move a card to **Doing** when you start it, and keep **no more than 2** cards in Doing at once (a *WIP limit*).
- Update your cards before the 09:15 scrum (held when time permits): *what I did · what I'm doing · blockers*.
- When a card meets the Definition of Done, move it to **Review**. The trainer moves it to **Done**.

---

## 3. The work

### Tabular datasets (two groups of four)

1. **Prepare the data:** handle missing values, encode categories, **scale** the numeric features (neural networks need it), and split into train / validation / test.
2. **Choose the right output:**
   - Classification: 1 output with a **sigmoid** + binary cross-entropy loss
   - Regression: 1 output with **no activation** + MSE loss
3. **Build at least 3 models**, for example:

| Model | Idea |
|---|---|
| Baseline MLP | 1–2 hidden layers, ReLU, Adam |
| Deeper DNN | More layers and units: does it overfit? |
| Regularised DNN | Add dropout and/or batch normalisation, plus early stopping |
| Optimiser / learning-rate runs | The same network with SGD vs Adam, and learning rates of 0.1 / 0.01 / 0.001 |

4. **Optional:** a Week 1 model (e.g. Random Forest) logged to MLflow too. Does deep learning actually beat it on tabular data?

### Image dataset (Toni)

1. **A simple CNN:** Conv → Pool → Conv → Pool → Dense.
2. **Deeper or regularised CNN:** more filters, dropout, data augmentation.
3. **A pretrained model** (transfer learning, e.g. MobileNet) compared with your CNN.
4. **Stretch goal, if time permits:** run a pretrained **Ultralytics YOLO** segmentation model on the `coco8-seg` sample, or on your own images, and show the predicted masks.

### Suggested setup (the simplest path)

**Keras** with MLflow's **autolog** keeps the code short:

```bash
uv add tensorflow mlflow pandas scikit-learn matplotlib
# If TensorFlow won't install, pin Python 3.12 first:  uv python pin 3.12
```

PyTorch is fine too if you prefer it.

---

## 4. Track experiments in MLflow

**Experiment tracking** means every training run is recorded automatically: the settings you used (**parameters**), the results (**metrics**), and the outputs (**artifacts**: plots, the model file). You can then compare runs side by side instead of losing them in notebook cells.

```python
import mlflow

mlflow.set_experiment("w2-<your-name>")
mlflow.autolog()                          # logs params, per-epoch metrics and the model automatically

with mlflow.start_run(run_name="mlp-2x64-adam-lr0.001"):
    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=30, batch_size=64)
    mlflow.log_param("hidden_layers", 2)  # add anything autolog doesn't capture
```

Then open the dashboard:

```bash
uv run mlflow ui        # then open http://127.0.0.1:5000
```

**What to log for each run:**
- **Parameters:** layers, units, activation, optimiser, learning rate, batch size, epochs, dropout
- **Metrics:** training and validation loss per epoch, plus your main metric (accuracy / F1 / ROC-AUC for classification; MAE / RMSE / R² for regression)
- **Artifacts:** the loss-curve plot and the trained model
- **A clear run name**, e.g. `dnn-4x128-dropout0.3`

**In the MLflow UI:** select your runs → **Compare** → look at the parameter and metric tables and the loss curves. Which run generalises best? Which overfit (training loss keeps falling while validation loss rises)?

Docs: [MLflow tracking](https://mlflow.org/docs/latest/ml/tracking/) · [Autolog](https://mlflow.org/docs/latest/ml/tracking/autolog/)

---

## 5. Push to GitHub

On your fork of this repository, on a branch called `week2/<your-name>`:

```
week2/<your-name>/
├── README.md        # dataset, models tried, results table, best model and why
├── train.py         # or a notebook: your code
└── screenshots/     # MLflow runs table, compare view, loss curves
```

- Add `mlruns/` and `mlartifacts/` to `.gitignore` (MLflow's local files), and **don't commit the dataset**. Link to it instead.
- `git add .` → `git commit -m "Add Week 2 DL experiments"` → `git push`
- Post the branch link on your cards.

---

## 6. Tuesday presentation

**Tuesday 20 October · 10 minutes per person.** No notebook walkthrough this time: slides plus your MLflow dashboard.

| Part | Content |
|---|---|
| **1. Problem and data** | The dataset, the target, and classification or regression |
| **2. Your sprint** | Show your cards: how you broke down the work, the acceptance criteria, what was done or blocked |
| **3. Models** | The architectures you tried (a small table) |
| **4. MLflow** | **Live or screenshots:** the runs table, the compare view, the loss curves |
| **5. Result** | The best model and **why**, with evidence from MLflow; signs of overfitting or underfitting; what you'd try next |

About 5 slides, plus the MLflow demo, plus 2 minutes for questions.

## Checklist

- [ ] My cards for this week are on the board, each with a description, acceptance criteria, label, due date and estimate
- [ ] At least 3 models trained and logged in MLflow, with clear run names
- [ ] Runs compared in MLflow, and the best model chosen with evidence
- [ ] Code, README and screenshots pushed to `week2/<your-name>`
- [ ] Every card meets the Definition of Done and is in **Review**
- [ ] Presentation ready for Tuesday 20 October
