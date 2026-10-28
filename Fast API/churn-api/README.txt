# Week 3: Adult Census Income Model Deployment

## 1. Project Overview

This project focuses on deploying a trained Machine Learning model using **FastAPI, Streamlit, and MLflow**.

The model uses the Adult Census Income dataset to predict whether a person's income is above $50K or at or below $50K based on personal and employment information.

## 2. Project Objectives

- Deploy a trained Machine Learning model using FastAPI.
- Create an interactive user interface using Streamlit.
- Use MLflow to manage and register the trained model.
- Connect Streamlit to FastAPI for real-time predictions.
- Return prediction probabilities and income categories.
- Understand how to serve a Machine Learning model through an API.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Pandas | Data handling |
| TensorFlow / Keras | Neural network model |
| Scikit-learn | Data preprocessing |
| Joblib | Saving and loading the preprocessor |
| MLflow | Experiment tracking and model registry |
| FastAPI | Creating the prediction API |
| Uvicorn | Running the API server |
| Streamlit | Creating the user interface |
| Git and GitHub | Version control |

## 4. Project Architecture

```text
              Adult Census Dataset
                       |
                       v
              Data Preprocessing
                       |
                       v
              Jupyter Notebook
              Model Training
                       |
                       v
                 MLflow
              Model Registry
                       |
                       v
                 FastAPI
               Prediction API
                       |
                       v
                 Streamlit
                User Interface
                       |
                       v
             Predicted Income Category
```

## 5. Dataset Description

The project uses the Adult Census Income dataset.

The model receives 14 input features, including:

- Age
- Workclass
- Final weight (`fnlwgt`)
- Education
- Education number
- Marital status
- Occupation
- Relationship
- Race
- Sex
- Capital gain
- Capital loss
- Hours per week
- Native country

**Target variable:** Income

The classification categories are:
- `<=50K`: Income at or below $50K
- `>50K`: Income above $50K

## 6. Model and Preprocessing

The trained neural network model is saved as:

```text
adult_census_best_model.keras
```

The preprocessing pipeline is saved as:

```text
adult_census_preprocessor.joblib
```

The preprocessor transforms the input data into the format expected by the trained model.

Both the model and the preprocessor are required to generate predictions correctly.

## 7. MLflow Model Registry

MLflow is used to track experiments and manage the registered model.

Registered model name:

```text
AdultCensusIncomeModel
```

Current registered version:

```text
Version 3
```

Model alias:

```text
champion
```

Version 3 is marked as the Champion model in the registry.

## 8. FastAPI Deployment

FastAPI provides endpoints for interacting with the model.

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Check whether the API is running |
| `/health` | GET | Check API health and model loading |
| `/model-info` | GET | Display model information |
| `/predict` | POST | Generate an income prediction |

### Example prediction request

```json
{
  "features": {
    "age": 82,
    "workclass": "Private",
    "fnlwgt": 132870,
    "education": "HS-grad",
    "education.num": 9,
    "marital.status": "Widowed",
    "occupation": "Exec-managerial",
    "relationship": "Not-in-family",
    "race": "White",
    "sex": "Female",
    "capital.gain": 2174,
    "capital.loss": 4356,
    "hours.per.week": 18,
    "native.country": "United-States"
  }
}
```

### Example API response

```json
{
  "prediction": [
    [
      0.4506241083
    ]
  ]
}
```

The model output is approximately 45.06%.

The Streamlit application uses a threshold of 0.5 to convert the probability into a binary prediction.

**Note:** The response contains a probability score. The interpretation of that score depends on how the target variable was encoded during training.

## 9. Streamlit Application

Streamlit provides an interactive interface where users can enter the 14 input features.

The application:

1. Collects user information.
2. Sends the input data to FastAPI as a JSON request.
3. Receives the model's prediction.
4. Displays the probability score.
5. Displays the predicted income category.

Streamlit communicates with FastAPI at:

```text
http://127.0.0.1:8000
```

## 10. How to Run the Project

### Step 1: Start FastAPI

Open a terminal in your existing `churn-api` project folder.

Activate the Python 3.13 environment that supports your TensorFlow installation:

```powershell
& "C:\Users\tejas\OneDrive\week0\ds-october-2026-week2\week2\.venv313\Scripts\Activate.ps1"
```

Set the model paths and disable MLflow loading if you want to use the local Keras model:

```powershell
$env:USE_MLFLOW="false"
$env:MODEL_PATH="C:\Users\tejas\OneDrive\week0\ds-october-2026-week2\week2\adult_census_best_model.keras"
$env:PREPROCESSOR_PATH="C:\Users\tejas\OneDrive\week0\ds-october-2026-week2\week2\adult_census_preprocessor.joblib"
```

Run the API from the directory containing your `app` folder:

```powershell
python -m uvicorn app.main:app --reload
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

### Step 2: Start Streamlit

Open a second terminal and navigate to the folder containing `streamlit_app.py`.

Activate the same Python environment, if needed, and run:

```powershell
python -m streamlit run streamlit_app.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser.

**Important:** The local-model configuration above is an alternative to loading the registered model from MLflow. If you want to use MLflow, configure its tracking URI and model settings instead.

## 11. Testing

The following components can be tested:

- FastAPI health endpoint.
- Model loading and model information.
- Prediction endpoint through Swagger UI.
- Streamlit connection to FastAPI.
- Prediction probability and displayed income category.
- MLflow model registration.

## 12. Challenges and Learning

During this project, I worked on:

- Connecting a trained model to FastAPI.
- Loading the saved model and preprocessing pipeline.
- Connecting Streamlit to the API.
- Testing predictions through Swagger UI.
- Managing a registered model using MLflow.
- Troubleshooting Python environments and dependency issues.
- Understanding how a trained model can be used in an application.

## 13. Conclusion

This project demonstrates how a trained Machine Learning model can be deployed as an application.

FastAPI handles prediction requests, Streamlit provides the user interface, and MLflow manages the registered model.

The project helped me understand the process of moving from model training to model deployment and testing.

## 14. Future Improvements

- Add input validation and clearer error messages.
- Improve model monitoring and experiment tracking.
- Use the MLflow Champion alias for dynamic model loading.
- Add automated API tests.
- Containerise the application using Docker.
- Improve the user interface and prediction reporting.