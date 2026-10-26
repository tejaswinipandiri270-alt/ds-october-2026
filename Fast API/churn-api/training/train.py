
from pathlib import Path

import joblib
from sklearn.dummy import DummyClassifier
from sklearn.datasets import make_classification

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)
python -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__)"

X, y = make_classification(
    n_samples=1000,
    n_features=5,
    random_state=42
)

model = DummyClassifier(strategy="most_frequent")
model.fit(X, y)

joblib.dump(model, MODEL_DIR / "churn_model.joblib")

print("Model trained and saved successfully!")