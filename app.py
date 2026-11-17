
import streamlit as st
import pandas as pd
import joblib

# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------

st.set_page_config(
    page_title="CNC Surface Roughness Prediction",
    page_icon="⚙️",
    layout="centered"
)

# ---------------------------------
# LOAD TRAINED MODEL
# ---------------------------------

try:
    model = joblib.load("best_model.pkl")
    feature_columns = joblib.load("feature_columns.pkl")

except Exception as e:
    st.error(f"Model loading error: {e}")
    st.stop()

# ---------------------------------
# APPLICATION TITLE
# ---------------------------------

st.title("⚙️ CNC Surface Roughness Prediction")

st.write("""
Welcome to the CNC Surface Roughness Prediction System.

This application uses a Machine Learning model to predict
surface roughness based on selected CNC machining parameters.
""")

st.divider()

# ---------------------------------
# USER GUIDELINES
# ---------------------------------

st.subheader("📌 User Guidelines")

st.info("""
1. Enter the Depth of Cut within the given range.
2. Select the required Cutting Speed.
3. Select the required Feed Rate.
4. Click the Predict Surface Roughness button.
5. View your predicted result and its interpretation.
""")

# ---------------------------------
# MACHINING PARAMETERS
# ---------------------------------

st.subheader("🔧 Enter Machining Parameters")

ap = st.number_input(
    "Depth of Cut (mm)",
    min_value=0.25,
    max_value=0.80,
    value=0.50,
    step=0.05,
    help="Depth of material removed during cutting."
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

# ---------------------------------
# PREDICTION SECTION
# ---------------------------------

if st.button(
    "🔍 Predict Surface Roughness",
    use_container_width=True
):

    try:
        # Prepare input data

        input_data = pd.DataFrame(
            [[ap, vc, f]],
            columns=["ap", "vc", "f"]
        )

        # Match model feature order

        input_data = input_data[feature_columns]

        # Make prediction

        prediction = model.predict(input_data)[0]

        # ---------------------------------
        # DISPLAY RESULT
        # ---------------------------------

        st.subheader("📊 Prediction Result")

        st.metric(
            label="Predicted Surface Roughness",
            value=f"{prediction:.4f} µm"
        )

        st.success("Prediction completed successfully!")

        # ---------------------------------
        # RESULT INTERPRETATION
        # ---------------------------------

        st.subheader("💡 Result Interpretation")

        st.write(
            f"Based on the selected machining parameters, "
            f"the predicted surface roughness is "
            f"{prediction:.4f} µm."
        )

        st.info("""
        **Understanding Surface Roughness**

        - Lower Ra values generally indicate smoother surfaces.
        - Higher Ra values generally indicate rougher surfaces.
        - The acceptable roughness depends on the component's
          application and required surface finish.
        """)

        # ---------------------------------
        # DISPLAY SELECTED PARAMETERS
        # ---------------------------------

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

        # ---------------------------------
        # FINAL NOTE
        # ---------------------------------

        st.caption("""
        Note: Predictions are generated using the trained
        Machine Learning model. Actual machining results may
        vary depending on machine, tool and material conditions.
        """)

    except Exception as e:
        st.error(f"Prediction error: {e}")

# ---------------------------------
# FOOTER
# ---------------------------------

st.divider()

st.caption(
    "CNC Surface Roughness Prediction | "
    "Machine Learning Based Application"
)

