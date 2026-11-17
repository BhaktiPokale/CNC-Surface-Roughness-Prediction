
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

/* Main Background */
.stApp {
    background: linear-gradient(
        135deg,
        #101B2D 0%,
        #14263D 55%,
        #193653 100%
    );
    color: #EAF3F8;
}

/* Main Container */
.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Headings */
h1, h2, h3 {
    color: #19C5D8 !important;
    font-weight: 800 !important;
}

/* Normal Text */
p, label, li {
    color: #D6E4EF !important;
}

/* Header */
header[data-testid="stHeader"] {
    background: transparent;
}

/* Hero Banner */
.hero {
    background: linear-gradient(
        120deg,
        #193653,
        #244966,
        #147C91
    );
    padding: 35px;
    border-radius: 20px;
    border: 1px solid #19C5D8;
    margin-bottom: 25px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
}

.hero h1 {
    color: #FFFFFF !important;
    font-size: 36px !important;
}

.hero p {
    color: #C9EAF0 !important;
    font-size: 16px;
}

/* Cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(25, 54, 83, 0.85);
    border: 1px solid #365B78;
    border-radius: 16px;
}

/* Metric Cards */
div[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        #193653,
        #244966
    );
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

/* Input Fields */
div[data-baseweb="select"] > div {
    background-color: #193653;
    border: 1px solid #19C5D8;
    border-radius: 10px;
}

div[data-baseweb="input"] > div {
    background-color: #193653;
    border: 1px solid #19C5D8;
    border-radius: 10px;
}

input {
    color: #FFFFFF !important;
}

/* Prediction Button */
.stButton > button {
    background: linear-gradient(
        90deg,
        #19C5D8,
        #00A6C7
    );
    color: #101B2D !important;
    border: none;
    border-radius: 12px;
    padding: 14px;
    font-size: 17px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton > button:hover {
    background: #FFFFFF;
    color: #101B2D !important;
    border: 1px solid #19C5D8;
}

/* Alerts */
.stAlert {
    border-radius: 12px;
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
        step=0.05,
        help="Enter the depth of material removed."
    )

with col2:

    vc = st.selectbox(
        "⚡ Cutting Speed (m/min)",
        [310, 350, 390],
        help="Select the cutting speed."
    )

with col3:

    f = st.selectbox(
        "🔧 Feed Rate (mm/rev)",
        [0.07, 0.10, 0.13],
        help="Select the feed rate per revolution."
    )

st.markdown("---")

# ==========================================
# PREDICTION SECTION
# ==========================================

if st.button(
    "🔍 PREDICT SURFACE ROUGHNESS",
    use_container_width=True
):

    try:

        # Prepare input data

        input_data = pd.DataFrame(
            [[ap, vc, f]],
            columns=["ap", "vc", "f"]
        )

        # Match training feature order

        input_data = input_data[feature_columns]

        # Generate prediction

        prediction = float(
            model.predict(input_data)[0]
        )

        if not pd.notna(prediction):
            raise ValueError("Invalid prediction returned by model.")

        # ==================================
        # PREDICTION RESULT
        # ==================================

        st.subheader("📊 Prediction Result")

        st.metric(
            label="Predicted Surface Roughness (Ra)",
            value=f"{prediction:.4f} µm"
        )

        st.success("Prediction completed successfully!")

        # ==================================
        # SURFACE FINISH ASSESSMENT
        # ==================================

        st.subheader("🔍 Surface Finish Assessment")

        # Provisional thresholds.
        # Validate against project specifications.

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

        # ==================================
        # RESULT EXPLANATION
        # ==================================

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

        # ==================================
        # SELECTED PARAMETERS
        # ==================================

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

        # ==================================
        # IMPORTANT NOTE
        # ==================================

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
