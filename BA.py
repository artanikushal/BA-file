# ==========================
# 🎓 NMIMS Loan Default Predictor Dashboard
# Problem 2: Credit Risk Evaluation – Current Default
# ==========================

import streamlit as st
import numpy as np
from PIL import Image

# --------------------------
# 🏠 Page setup
# --------------------------
st.set_page_config(page_title="Credit Risk Evaluation - Current Default", layout="wide")

# --------------------------
# 🎨 Custom CSS
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
        .st-emotion-cache-18ni7ap {
            visibility: hidden; /* Hide Streamlit settings menu */
        }
    </style>
""", unsafe_allow_html=True)

# --------------------------
# 🧾 Header Section
# --------------------------
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
    income = st.text_input("Monthly Income (₹)", value="50000")
    employment = st.selectbox("Employment Status", ["Salaried", "Self Employed", "Unemployed"])
    location = st.selectbox("Location", ["Urban", "Rural"])

with col2:
    loan_type = st.selectbox("Loan Type", ["Car", "Home", "Personal"])
    rating = st.selectbox("Credit Score Rating", ["Good", "Bad"])

# --------------------------
# 🔢 Input Processing
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
loan_home = 1 if loan_type == "Home
