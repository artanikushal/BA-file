import streamlit as st
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="Credit Risk Evaluation", layout="wide")

# --- Custom CSS for styling ---
st.markdown("""
<style>
    body {
        background-color: #f9f9f9;
        color: #222;
    }
    .main-header {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: white;
        padding: 25px 0;
        border-bottom: 2px solid #eee;
        position: fixed;
        top: 0;
        width: 100%;
        z-index: 999;
    }
    .main-header img {
        height: 90px;
        margin-right: 20px;
    }
    .main-header h1 {
        font-size: 42px;
        font-weight: 750;
        letter-spacing: 0.5px;
        margin: 0;
    }
    .content {
        margin-top: 160px;
        padding: 20px;
    }
    .stButton > button {
        display: block;
        margin: 40px auto;
        font-size: 18px !important;
        font-weight: 600;
        background-color: #2b7de9 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px;
        padding: 12px 40px;
    }
    .output-text {
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        margin-top: 35px;
    }
</style>
""", unsafe_allow_html=True)

# --- Header with logo ---
st.markdown(
    """
    <div class='main-header'>
        <img src='https://raw.githubusercontent.com/kushalartani/assets/main/logo.png'>
        <h1>CREDIT RISK EVALUATION</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Main content ---
st.markdown("<div class='content'>", unsafe_allow_html=True)
st.subheader("Enter Customer Details")

col1, col2, col3 = st.columns(3)

with col1:
    employment_status = st.selectbox("Employment Status", ["Salaried", "Self Employed", "Unemployed"])
    loan_type = st.selectbox("Loan Type", ["Car", "Home", "Personal"])

with col2:
    credit_score = st.selectbox("Credit Score Rating", ["Good", "Bad"])
    location = st.selectbox("Location", ["Urban", "Rural"])

with col3:
    monthly_income = st.number_input("Monthly Income", min_value=1000, step=100, value=30000)

# --- Encode categorical variables (base levels aligned with model coefficients) ---
income = monthly_income

# Employment status: Salaried as base
emp_self = 1 if employment_status == "Self Employed" else 0
emp_unemp = 1 if employment_status == "Unemployed" else 0

# Loan type: Car as base
loan_home = 1 if loan_type == "Home" else 0
loan_personal = 1 if loan_type == "Personal" else 0

# Credit Score Rating: Bad as base
credit_good = 1 if credit_score == "Good" else 0

# Location: Rural as base
loc_urban = 1 if location == "Urban" else 0

# --- Logistic Regression Coefficients (from your data) ---
intercept = 5.3551976259790495
coef_income = -0.0000259617687418
coef_emp_self = 1.6580628910103044
coef_emp_unemp = 4.4818219836163369
coef_loan_home = -2.4986504193573835
coef_loan_personal = 1.6928703494225534
coef_credit_good = -4.6784777493614556
coef_loc_urban = -1.5705748584574404

# --- Logistic regression calculation ---
log_odds = (
    intercept
    + coef_income * income
    + coef_emp_self * emp_self
    + coef_emp_unemp * emp_unemp
    + coef_loan_home * loan_home
    + coef_loan_personal * loan_personal
    + coef_credit_good * credit_good
    + coef_loc_urban * loc_urban
)
prob_default = 1 / (1 + np.exp(-log_odds))

# --- Display result ---
if st.button("Predict Credit Risk"):
    if prob_default >= 0.5:
        st.markdown("<p class='output-text' style='color:red;'>RISKY</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p class='output-text' style='color:green;'>NOT RISKY</p>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
