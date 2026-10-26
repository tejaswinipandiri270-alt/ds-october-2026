

import streamlit as st
import requests

st.set_page_config(page_title="Adult Census Income Prediction", page_icon="📊")

st.title("Adult Census Income Prediction")
st.write("Enter a person's details to predict their income category.")
API_URL = "http://api:8000"
st.subheader("Personal Information")

age = st.number_input("Age", min_value=17, max_value=100, value=39)

workclass = st.selectbox(
    "Workclass",
    ["Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov",
     "Local-gov", "State-gov", "Without-pay", "Never-worked", "?"]
)

fnlwgt = st.number_input("Final Weight (fnlwgt)", min_value=0, value=77516)

education = st.selectbox(
    "Education",
    ["Bachelors", "HS-grad", "Some-college", "Masters", "Assoc-voc",
     "11th", "Assoc-acdm", "10th", "7th-8th", "Prof-school",
     "9th", "12th", "Doctorate", "5th-6th", "1st-4th",
     "Preschool"]
)

education_num = st.number_input(
    "Education Number", min_value=0, max_value=16, value=13
)

marital_status = st.selectbox(
    "Marital Status",
    ["Never-married", "Married-civ-spouse", "Divorced",
     "Married-spouse-absent", "Separated", "Widowed",
     "Married-AF-spouse"]
)

occupation = st.selectbox(
    "Occupation",
    ["Adm-clerical", "Exec-managerial", "Handlers-cleaners",
     "Prof-specialty", "Other-service", "Sales", "Craft-repair",
     "Transport-moving", "Farming-fishing", "Machine-op-inspct",
     "Tech-support", "Protective-serv", "Armed-Forces",
     "Priv-house-serv", "?"]
)

relationship = st.selectbox(
    "Relationship",
    ["Not-in-family", "Husband", "Wife", "Own-child",
     "Unmarried", "Other-relative"]
)

race = st.selectbox(
    "Race",
    ["White", "Black", "Asian-Pac-Islander", "Amer-Indian-Eskimo",
     "Other"]
)

sex = st.selectbox("Sex", ["Male", "Female"])

capital_gain = st.number_input("Capital Gain", min_value=0, value=0)
capital_loss = st.number_input("Capital Loss", min_value=0, value=0)

hours_per_week = st.number_input(
    "Hours Per Week", min_value=1, max_value=100, value=40
)

native_country = st.selectbox(
    "Native Country",
    ["United-States", "Mexico", "India", "Canada", "England",
     "Germany", "Philippines", "Other"]
)

st.divider()

if st.button("Check API Connection"):
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.ok:
            st.success("FastAPI is connected!")
        else:
            st.error(f"API returned status code: {response.status_code}")
    except requests.RequestException as exc:
        st.error(f"Could not connect to FastAPI: {exc}")

if st.button("Predict Income", type="primary"):
    payload = {
        "age": age,
        "workclass": workclass,
        "fnlwgt": fnlwgt,
        "education": education,
        "education.num": education_num,
        "marital.status": marital_status,
        "occupation": occupation,
        "relationship": relationship,
        "race": race,
        "sex": sex,
        "capital.gain": capital_gain,
        "capital.loss": capital_loss,
        "hours.per.week": hours_per_week,
        "native.country": native_country,
    }

    try:
        with st.spinner("Getting prediction from the model..."):
            response = requests.post(
               f"{API_URL}/predict",
               json={"features": payload},
                timeout=30,
            )
        
        if response.ok:
            result = response.json()

            # Extract the model's probability score
            probability = float(result["prediction"][0][0])

            # Apply a 0.5 threshold to get a binary class
            predicted_class = 1 if probability >= 0.5 else 0

            if predicted_class == 1:
                st.success("Prediction: Income above $50K")
            else:
                st.info("Prediction: Income at or below $50K")

            st.metric(
                "Model output probability",
                f"{probability:.2%}",
            )

            st.caption(
                "This is a model prediction, not a guarantee of actual income."
            )

        else:
            st.error(f"Prediction failed ({response.status_code})")
            st.code(response.text)

    except requests.RequestException as exc:
        st.error(f"Could not reach FastAPI: {exc}")