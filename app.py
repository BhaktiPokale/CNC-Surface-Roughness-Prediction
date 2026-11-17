
import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("best_model.pkl")
feature_columns = joblib.load("feature_columns.pkl")

# Page settings
st.set_page_config(
    page_title="CNC Surface Roughness Prediction",
    page_icon="⚙️",
    layout="centered"
)

# Title
st.title("⚙️ CNC Surface Roughness Prediction")

st.write("""
This application predicts the surface roughness of a CNC machined
component based on machining parameters using Machine Learning.
""")

st.divider()

# Guidelines
st.subheader("📌 User Guidelines")

st.info("""
1. Enter the Depth of Cut within the specified range.
2. Select the required Cutting Speed.
3. Select the required Feed Rate.
4. Click the Predict button to calculate surface roughness.
5. View the predicted result and its interpretation below.
""")

# Input section
st.subheader("🔧 Enter Machining Parameters")

ap = st.number_input(
    "Depth of Cut (mm)",
    min_value=0.25,
    max_value=0.80,
    value=0.50,
    step=0.05,
    help="Enter the depth of material removed during one cutting pass."
)

vc = st.selectbox(
    "Cutting Speed (m/min)",
    [310, 350, 390],
    help="Select the cutting speed of the tool."
)

f = st.selectbox(
    "Feed Rate (mm/rev)",
    [0.07, 0.10, 0.13],
    help="Select the feed rate per revolution."
)

st.divider()

# Prediction
if st.button("🔍 Predict Surface Roughness", use_container_width=True):

    input_data = pd.DataFrame(
        [[ap, vc, f]],
        columns=["ap", "vc", "f"]
    )

    input_data = input_data[feature_columns]

    prediction = model.predict(input_data)[0]

    st.subheader("📊 Prediction Result")

    st.metric(
        label="Predicted Surface Roughness",
        value=f"{prediction:.4f} µm"
    )

    st.success("Prediction completed successfully!")

    # Interpretation
    st.subheader("💡 Result Interpretation")

    st.write(
        f"Based on the selected machining parameters, "
        f"the predicted surface roughness is {prediction:.4f} µm."
    )

    st.info("""
    **What does this result mean?**

    - Surface roughness indicates the quality and smoothness
      of the machined surface.
    - A lower Ra value generally indicates a smoother surface.
    - A higher Ra value generally indicates a rougher surface.
    """)

    st.subheader("⚙️ Selected Machining Parameters")

    result_table = pd.DataFrame({
        "Parameter": [
            "Depth of Cut",
            "Cutting Speed",
            "Feed Rate"
        ],
        "Selected Value": [
            f"{ap} mm",
            f"{vc} m/min",
            f"{f} mm/rev"
        ]
    })

    st.table(result_table)

    st.caption(
        "Note: This prediction is based on the trained "
        "machine learning model. Actual machining results "
        "may vary depending on machine and tool conditions."
    )

# Footer
st.divider()

st.caption(
    "CNC Surface Roughness Prediction | "
    "Machine Learning Based Application"
)


    prediction = model.predict(input_data)

    st.success(f"Predicted Surface Roughness: {prediction[0]:.4f} µm")
