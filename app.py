
import streamlit as st
import pandas as pd
import joblib

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="CNC Surface Roughness Prediction",
    page_icon="⚙️",
    layout="wide"
)

# ==========================================
# MIDNIGHT BLUE THEME
# ==========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #101B2D, #14263D, #193653);
    color: #EAF3F8;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #19C5D8 !important;
    font-weight: 800 !important;
}

p, label, li {
    color: #D6E4EF !important;
}

header[data-testid="stHeader"] {
    background: transparent;
}

/* Hero Banner */
.hero {
    background: linear-gradient(120deg, #193653, #244966, #147C91);
    padding: 35px;
    border-radius: 20px;
    border: 1px solid #19C5D8;
    margin-bottom: 25px;
}

.hero h1 {
    color: #FFFFFF !important;
    font-size: 36px !important;
}

.hero p {
    color: #C9EAF0 !important;
}

/* Cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(25, 54, 83, 0.85);
    border: 1px solid #365B78;
    border-radius: 16px;
}

/* Metric */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #193653, #244966);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #19C5D8;
}

div[data-testid="stMetricLabel"] {
    color: #B7D6E5 !important;
}

div[data-testid="stMetricValue"] {
    color: #19C5D8 !important;
    font-weight: 800;
}

/* Input Boxes */
div[data-baseweb="input"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #19C5D8;
    border-radius: 10px;
}

div[data-baseweb="input"] input {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    background-color: #FFFFFF !important;
}

/* Dropdown Boxes */
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #19C5D8;
    border-radius: 10px;
}

div[data-baseweb="select"] input {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

div[data-baseweb="select"] span {
    color: #000000 !important;
}

/* Prediction Button */
.stButton > button {
    background: linear-gradient(90deg, #19C5D8, #00A6C7);
    color: #101B2D !important;
    border: none;
    border-radius: 12px;
    padding: 14px;
    font-size: 17px;
    font-weight: bold;
}

.stButton > button:hover {
    background: #FFFFFF;
    color: #101B2D !important;
}

/* SUCCESS, WARNING AND ERROR MESSAGES: BLACK TEXT */
div[data-testid="stAlert"] {
    background-color: #FFFFFF !important;
    border: 1px solid #19C5D8 !important;
    border-radius: 12px;
}

div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span,
div[data-testid="stAlert"] li {
    color: #000000 !important;
}

/* Important Note */
div[data-testid="stAlert"] strong {
    color: #000000 !important;
}

/* Tables */
div[data-testid="stDataFrame"] {
    border: 1px solid #365B78;
    border-radius: 12px;
}

/* Divider */
hr {
    border-color: #365B78;
}

/* Footer */
.footer {
    text-align: center;
    color: #A9C3D4;
    padding: 20px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD TRAINED MODEL
# ==========================================

try:
    model = joblib.load("best_model.pkl")
    feature_columns = joblib.load("feature_columns.pkl")

except Exception as e:
    st.error(f"Model loading error: {e}")
    st.stop()

# ==========================================
# HERO SECTION
# ==========================================

st.markdown("""
<div class="hero">
    <h1>⚙️ CNC Surface Roughness Prediction</h1>
    <p>
        Intelligent machining analysis powered by
        Machine Learning.
        Predict and understand your CNC surface finish.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# USER GUIDELINES
# ==========================================

with st.container(border=True):

    st.subheader("📌 Welcome to Your Prediction Dashboard")

    st.write("""
    This application predicts the surface roughness
    of CNC machined components using Machine Learning.

    **How to use this application:**

    1. Enter the Depth of Cut.
    2. Select the Cutting Speed.
    3. Select the Feed Rate.
    4. Click the Predict button.
    5. View the predicted surface roughness.
    6. Check the surface finish assessment.
    """)

# ==========================================
# MACHINING PARAMETERS
# ==========================================

st.subheader("⚙️ Machining Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    ap = st.number_input(
        "📏 Depth of Cut (mm)",
        min_value=0.25,
        max_value=0.80,
        value=0.50,
        step=0.05
    )


with col2:
    vc = st.number_input(
        "⚡ Cutting Speed (m/min)",
        min_value=310.0,
        max_value=390.0,
        value=350.0,
        step=1.0
    )

with col3:
    f = st.number_input(
        "🔧 Feed Rate (mm/rev)",
        min_value=0.07,
        max_value=0.13,
        value=0.10,
        step=0.001,
        format="%.3f"
    )


st.markdown("---")

# ==========================================
# PREDICTION SECTION
# ==========================================

if st.button("🔍 PREDICT SURFACE ROUGHNESS", use_container_width=True):

    try:

        input_data = pd.DataFrame(
            [[ap, vc, f]],
            columns=["ap", "vc", "f"]
        )

        input_data = input_data[feature_columns]

        prediction = float(model.predict(input_data)[0])

        if not pd.notna(prediction):
            raise ValueError("Invalid prediction returned by model.")

        # Prediction Result

        st.subheader("📊 Prediction Result")

        st.metric(
            label="Predicted Surface Roughness (Ra)",
            value=f"{prediction:.4f} µm"
        )

        st.success("Prediction completed successfully!")

        # Surface Finish Assessment

        st.subheader("🔍 Surface Finish Assessment")

        if prediction < 0.8:

            st.success("🟢 SMOOTH SURFACE")

            st.write("""
            The predicted surface has relatively low
            roughness and indicates a smoother finish.
            """)

        elif prediction < 1.6:

            st.warning("🟡 MODERATELY ROUGH SURFACE")

            st.write("""
            The predicted surface has a moderate
            level of roughness.
            """)

        else:

            st.error("🔴 ROUGH SURFACE")

            st.write("""
            The predicted surface has relatively high
            roughness and indicates a rougher finish.
            """)

        # Result Explanation

        st.subheader("💡 Understanding Your Result")

        left, right = st.columns(2)

        with left:
            with st.container(border=True):
                st.markdown("### 🌊 Smoother Surface")
                st.write("""
                A lower Ra value generally indicates
                a smoother machined surface with
                smaller surface irregularities.
                """)

        with right:
            with st.container(border=True):
                st.markdown("### ⚙️ Rougher Surface")
                st.write("""
                A higher Ra value generally indicates
                a rougher machined surface with
                larger surface irregularities.
                """)

        # Selected Parameters

        st.subheader("⚙️ Selected Machining Parameters")

        result_table = pd.DataFrame({
            "Machining Parameter": [
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

        st.dataframe(
            result_table,
            use_container_width=True,
            hide_index=True
        )

        # Important Note

        st.info("""
        **Important Note**

        Predictions are generated using the trained
        Machine Learning model.

        Actual machining results may vary depending
        on machine, tool and material conditions.

        Surface finish categories use provisional
        thresholds and should be validated against
        the required surface finish specifications.
        """)

    except Exception as e:
        st.error(f"Prediction error: {e}")

# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<hr>

<div class="footer">
    ⚙️ CNC Surface Roughness Prediction<br>
    Machine Learning Based Application<br>
    Intelligent CNC Machining Analysis
</div>
""", unsafe_allow_html=True)
