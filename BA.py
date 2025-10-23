# ==========================
# 🎓 NMIMS Loan Default Predictor Dashboard
# ==========================

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from PIL import Image

# --------------------------
# 🏠 Page setup
# --------------------------
st.set_page_config(page_title="NMIMS Loan Default Predictor", page_icon="nmims-university-logo.png", layout="wide")

# --------------------------
# 📘 Header with logo
# --------------------------
col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.markdown("<h1 style='color:#800000;'>NMIMS Loan Default Risk Predictor</h1>", unsafe_allow_html=True)
    st.markdown("This dashboard predicts the likelihood of loan default based on borrower details.")
with col2:
    try:
        logo = Image.open("nmims-university-logo.png")
        st.image(logo, width=120)
    except:
        st.warning("NMIMS Logo not found — please ensure 'nmims-university-logo.png' is in the same folder.")

st.markdown("---")

# --------------------------
# 🧮 User Inputs
# --------------------------
st.subheader("Enter Customer Details")

col1, col2 = st.columns(2)
with col1:
    income = st.text_input("Monthly Income (₹)", value="50000")
    employment = st.selectbox("Employment Status", ["Salaried", "Self Employed"])
with col2:
    location = st.selectbox("Location", ["Urban", "Rural"])
    loan_type = st.selectbox("Loan Type", ["Home", "Personal"])
    rating = st.selectbox("Credit Rating", ["Good", "Bad"])

st.markdown("---")

# --------------------------
# 🧠 Logistic Regression Model (Based on your estimates)
# --------------------------
# Intercept = 7.8038
# Income = -0.0000117906553604
# Personal – Home = 2.1736
# Self Employed – Salaried = 1.2768
# Urban – Rural = -2.4431
# Good – Bad = -2.5169

try:
    income_val = float(income)
except:
    st.error("Please enter a valid number for Monthly Income.")
    st.stop()

loan_val = 1 if loan_type == "Personal" else 0
emp_val = 1 if employment == "Self Employed" else 0
loc_val = 1 if location == "Urban" else 0
rating_val = 1 if rating == "Good" else 0

z = (
    7.8038
    + (-0.0000117906553604 * income_val)
    + (2.1736 * loan_val)
    + (1.2768 * emp_val)
    + (-2.4431 * loc_val)
    + (-2.5169 * rating_val)
)
prob_default = 1 / (1 + np.exp(-z))

# --------------------------
# 📊 Gauge Indicator (Default Risk)
# --------------------------
def draw_default_gauge(prob):
    color = "green" if prob < 0.5 else "red"
    label = "Low Risk" if prob < 0.5 else "High Risk"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob * 100,
        title={"text": f"Default Risk: {label}", "font": {"size": 22}},
        number={'suffix': "%", 'font': {'size': 32}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "black"},
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "gray",
            "steps": [
                {"range": [0, 50], "color": "lightgreen"},
                {"range": [50, 100], "color": "lightcoral"}
            ],
            "threshold": {
                "line": {"color": "black", "width": 4},
                "thickness": 0.8,
                "value": prob * 100
            }
        }
    ))

    fig.update_layout(
        margin={"t": 0, "b": 0, "l": 0, "r": 0},
        height=300,
    )
    return fig


# --------------------------
# 🚀 Predict Button
# --------------------------
if st.button("Predict Default Risk"):
    st.subheader("📈 Prediction Result")
    st.write(f"**Predicted Probability of Default:** {prob_default*100:.2f}%")

    if prob_default >= 0.5:
        st.error("⚠️ High risk of default detected.")
    else:
        st.success("✅ Low risk borrower.")

    st.plotly_chart(draw_default_gauge(prob_default), use_container_width=True)

