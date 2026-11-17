
import streamlit as st
import pandas as pd
import joblib

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="CNC Surface Roughness Prediction",
    page_icon="⚙️",
    layout="centered"
)

# --------------------------------
# LOAD TRAINED MODEL
# --------------------------------

try:
    model = joblib.load("best_model.pkl")
    feature_columns = joblib.load("feature_columns.pkl")

except Exception as e:
    st.error(f"Model loading error: {e}")
    st.stop()

# --------------------------------
# TITLE
# --------------------------------

st.title("⚙️ CNC Surface Roughness Prediction")

st.write("""
Welcome to the CNC Surface Roughness Prediction System.

This application uses Machine Learning to predict the
surface roughness of a CNC machined component based on
selected machining parameters.
""")

st.divider()

# --------------------------------
# USER GUIDELINES
# --------------------------------

st.subheader("📌 User Guidelines")

st.info("""
1. Enter the Depth of Cut.
2. Select the Cutting Speed.
3. Select the Feed Rate.
4. Click the Predict button.
5. View the predicted surface roughness.
6. Check whether the surface is Smooth,
   Moderately Rough, or Rough.
""")

# --------------------------------
# MACHINING PARAMETERS
# --------------------------------

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

# --------------------------------
# PREDICTION
# --------------------------------

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

        input_data = input_data[feature_columns]

        # Predict surface roughness

        prediction = float(model.predict(input_data)[0])

        # --------------------------------
        # DISPLAY PREDICTION
        # --------------------------------

        st.subheader("📊 Prediction Result")

        st.metric(
            label="Predicted Surface Roughness",
            value=f"{prediction:.4f} µm"
        )

        st.success("Prediction completed successfully!")

        # --------------------------------
        # SURFACE FINISH ASSESSMENT
        # --------------------------------

        st.subheader("🔍 Surface Finish Assessment")

        # Provisional thresholds:
        # Replace with validated project limits.

        if prediction < 0.8:

            st.success("🟢 SMOOTH SURFACE")

            st.write("""
            The predicted surface has relatively low
            roughness and indicates a smoother finish.
            """)

        elif prediction < 1.6:

            st.warning("🟡 MODERATELY ROUGH SURFACE")

            st.write("""
            The predicted surface has a moderate level
            of roughness.
            """)

        else:

            st.error("🔴 ROUGH SURFACE")

            st.write("""
            The predicted surface has relatively high
            roughness and indicates a rougher finish.
            """)

        # --------------------------------
        # SURFACE ROUGHNESS EXPLANATION
        # --------------------------------

        st.subheader("💡 Understanding the Result")

        st.info("""
        - Lower Ra value = Smoother surface.
        - Higher Ra value = Rougher surface.
        - Surface finish quality depends on the
          required application and specifications.
        """)

        # --------------------------------
        # SELECTED PARAMETERS
        # --------------------------------

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

        # --------------------------------
        # FINAL NOTE
        # --------------------------------

        st.caption("""
        Note: Results are generated using a trained
        Machine Learning model. Actual machining results
        may vary depending on machine, tool and material
        conditions. Surface finish categories use
        provisional thresholds and should be validated.
        """)

    except Exception as e:

        st.error(f"Prediction error: {e}")

# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.caption(
    "CNC Surface Roughness Prediction | "
    "Machine Learning Based Application"
)
