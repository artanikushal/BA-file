# ==========================
# 🎓 NMIMS Loan Default Predictor Dashboard (Problem 2: Credit Risk Evaluation – Current Default)
# ==========================

import streamlit as st
import numpy as np
from PIL import Image

# --------------------------
# 🏠 Page setup
# --------------------------
st.set_page_config(page_title="Credit Risk Evaluation - Current Default", layout="wide")

# --------------------------
# 📘 Fixed Header with Logo
# --------------------------
st.markdown("""
    <style>
        .fixed-header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: white;
            padding: 25px 60px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #800000;
            z-index: 999;
        }
        .header-title {
            color: #800000;
            font-size: 46px;
            font-weight: 700;
            font-family: 'Segoe UI', sans-serif;
        }
        .content {
            margin-top: 140px;
        }
        .predict-btn button {
            width: 230px !important;
            height: 60px !important;
            font-size: 20px !important;
            background-color: #800000 !important;
            color: white !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Fixed header HTML
st.markdown("""
    <div class="fixed-header">
        <div class="header-title">Credit Risk Evaluation – Current Default</div>
        <div>
            <img src="nmims-university-logo.png" width="140">
        </div>
    </div>
""", unsafe_allow_html=True)

# --------------------------
# 🧮 User Inputs
# --------------------------
st.markdown('<div class="content">', unsafe_allow_html=True)
st.subheader("Enter Applicant Details")

col1, col2 = st.columns(2)

with col1:
    income = st.text_input("Annual Income (₹)", value="600000")
    employment = st.selectbox("Employment Status", ["Salaried", "Self Employed", "Unemployed"])
    location = st.selectbox("Location", ["Urban", "Rural"])

with col2:
    loan_type = st.selectbox("Loan Type", ["Car", "Home", "Personal"])
    rating = st.selectbox("Credit Score Rating", ["Good", "Bad"])

# --------------------------
# 🧠 Logistic Regression Calculation
# --------------------------
try:
    income_val = float(income)
except:
    st.error("Please enter a valid numeric income value.")
    st.stop()

# Employment encoding (base = Salaried)
emp_self = 1 if employment == "Self Employed" else 0
emp_unemp = 1 if employment == "Unemployed" else 0

# Loan Type encoding (base = Car)
loan_home = 1 if loan_type == "Home" else 0
loan_personal = 1 if loan_type == "Personal" else 0

# Credit Rating encoding (base = Bad)
rating_good = 1 if rating == "Good" else 0

# Location encoding (base = Rural)
loc_urban = 1 if location == "Urban" else 0

# --------------------------
# 🔢 Logistic Regression Equation
# --------------------------
z = (
    5.3551976259790495
    + (-0.0000259617687418 * income_val)
    + (1.6580628910103044 * emp_self)
    + (4.4818219836163369 * emp_unemp)
    + (-2.4986504193573835 * loan_home)
    + (1.6928703494225534 * loan_personal)
    + (-4.6784777493614556 * rating_good)
    + (-1.5705748584574404 * loc_urban)
)

prob_default = 1 / (1 + np.exp(-z))

# --------------------------
# 🚀 Predict Button
# --------------------------
st.markdown("<br><br><div class='predict-btn' style='text-align:center;'>", unsafe_allow_html=True)
predict = st.button("Predict Current Default Risk")
st.markdown("</div>", unsafe_allow_html=True)

# --------------------------
# 🎯 Output Display
# --------------------------
if predict:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader("Prediction Result")

    if prob_default >= 0.5:
        st.markdown(
            f"<h2 style='color:red; font-weight:700;'>Risky Applicant</h2>"
            f"<h4>Predicted Probability of Default: {prob_default*100:.2f}%</h4>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<h2 style='color:green; font-weight:700;'>Not Risky</h2>"
            f"<h4>Predicted Probability of Default: {prob_default*100:.2f}%</h4>",
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)
