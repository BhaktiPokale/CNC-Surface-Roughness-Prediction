
import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load("best_model.pkl")

# Load feature columns
feature_columns = joblib.load("feature_columns.pkl")

st.title("CNC Surface Roughness Prediction")

st.write("Enter the CNC machining parameters below.")

# User inputs
ap = st.number_input("Depth of Cut (mm)", min_value=0.25, max_value=0.80, value=0.50)

vc = st.selectbox("Cutting Speed (m/min)", [310, 350, 390])

f = st.selectbox("Feed Rate (mm/rev)", [0.07, 0.10, 0.13])

if st.button("Predict Surface Roughness"):

    input_data = pd.DataFrame(
        [[ap, vc, f]],
        columns=["ap", "vc", "f"]
    )

    input_data = input_data[feature_columns]

    prediction = model.predict(input_data)

    st.success(f"Predicted Surface Roughness: {prediction[0]:.4f} µm")
