import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# --------------------------
# 🏠 Page setup
# --------------------------
st.set_page_config(page_title="NMIMS Loan Default Predictor", page_icon="🏦", layout="wide")

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
    except Exception:
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
# 🧠 Logistic Regression Model
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
# 📊 Semi-Circle Default Risk Indicator (Matplotlib)
# --------------------------
def draw_semi_circle(prob):
    fig, ax = plt.subplots(figsize=(5, 2.5))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(0, 1.2)
    ax.axis("off")

    # Draw background semicircle
    theta = np.linspace(0, np.pi, 200)
    ax.fill_between(np.cos(theta), 0, np.sin(theta), color="lightgray", alpha=0.3)

    # Determine color based on probability
    color = "green" if prob < 0.5 else "red"
    label = "Low Default Risk" if prob < 0.5 else "High Default Risk"

    # Draw filled risk indicator
    cutoff = prob * np.pi
    theta_fill = np.linspace(0, cutoff, 100)
    ax.fill_between(np.cos(theta_fill), 0, np.sin(theta_fill), color=color, alpha=0.7)

    # Add text
    ax.text(0, -0.15, f"Default Probability: {prob*100:.1f}%", 
            ha="center", fontsize=12, fontweight="bold")
    ax.text(0, 0.6, label, ha="center", fontsize=14, color=color, fontweight="bold")

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

    fig = draw_semi_circle(prob_default)
    st.pyplot(fig)
