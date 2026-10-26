
import os

import mlflow

import pandas as pd
import tensorflow as tf
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib

app = FastAPI()

# Select the model source.
USE_MLFLOW = os.getenv("USE_MLFLOW", "true").lower() == "true"

MODEL_PATH = os.getenv(
    "MODEL_PATH",
    "/week2/adult_census_best_model.keras",
)

model = None


if USE_MLFLOW:
    tracking_uri = os.getenv(
        "MLFLOW_TRACKING_URI",
        "http://mlflow:5000",
    )
    mlflow.set_tracking_uri(tracking_uri)

    model_name = os.getenv(
        "MODEL_NAME",
        "AdultCensusIncomeModel",
    )
    model_version = os.getenv("MODEL_VERSION", "3")

    model_uri = f"models:/{model_name}/{model_version}"

    try:
        model = mlflow.pyfunc.load_model(model_uri)
        print(f"Loaded model from MLflow Registry: {model_uri}")

    except Exception as e:
        print(f"MLflow Registry loading failed: {e}")
        raise RuntimeError(
            f"Could not load registered model: {model_uri}"
        ) from e

else:
    model = tf.keras.models.load_model(MODEL_PATH)
    print(f"Loaded local TensorFlow model: {MODEL_PATH}")


# Load the saved preprocessing pipelin
PREPROCESSOR_PATH = os.getenv(
    "PREPROCESSOR_PATH",
    "/week2/adult_census_preprocessor.joblib",
)

preprocessor = joblib.load(PREPROCESSOR_PATH)

print("Preprocessor loaded successfully.")


class PredictionRequest(BaseModel):
    features: dict


@app.get("/")
def home():
    return {"message": "Adult Census Income API is running"}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
    }

@app.get("/model-info")
def model_info():
    return {
        "model_loaded": model is not None,
        "model_name": os.getenv(
            "MODEL_NAME",
            "AdultCensusIncomeModel",
        ),
        "model_alias": os.getenv(
            "MODEL_ALIAS",
            "champion",
        ),
    }



@app.post("/predict")
def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model is not loaded",
        )

    try:
        # Create a DataFrame from the 14 raw input features
        input_data = pd.DataFrame([request.features])

        # Ensure columns appear in the order expected by the preprocessor
        input_data = input_data[list(preprocessor.feature_names_in_)]

        # Transform categorical and numerical features
        processed_data = preprocessor.transform(input_data)

        # Make the prediction using the existing MLflow model
        prediction = model.predict(processed_data)

        return {
            "prediction": prediction.tolist()
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Prediction failed: {str(e)}",
        )
