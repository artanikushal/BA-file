import streamlit as st
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="Credit Risk Evaluation", layout="wide")

# --- Remove Streamlit’s default menu, footer, etc. ---
hide_default_format = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
"""
st.markdown(hide_default_format, unsafe_allow_html=True)

# --- Custom CSS for styling ---
st.markdown("""
<style>
    body {
        background-color: #f4f6f9;
        color: #222;
        font-family: "Segoe UI", sans-serif;
    }
    .main-header {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: white;
        padding: 25px 0;
        border-bottom: 3px solid #eee;
        position: fixed;
        top: 0;
        width: 100%;
        z-index: 999;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
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
        color: #003366;
    }
    .content {
        margin-top: 180px;
        padding: 20px 60px;
    }
    .stSelectbox label, .stNumberInput label {
        font-weight: 600 !important;
        font-size: 16px !important;
        color: #003366 !important;
    }
    .stSelectbox, .stNumberInput {
        background: #ffffff;
        border-radius: 12px !important;
        padding: 10px 20px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    }
    .stButton > button {
        display: block;
        margin: 50px auto 0;
        font-size: 20px !important;
        font-weight: 600;
        background-color: #2b7de9 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px;
        padding: 14px 60px;
        box-shadow: 0 4px 10px rgba(43,125,233,0.3);
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        background-color: #1a5fc1 !important;
        transform: scale(1.03);
    }
    .output-container {
        margin-top: 50px;
        text-align: center;
    }
    .output-text {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: 1px;
        text-align: center;
        margin-top: 20px;
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

# --- Main content section ---
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

# --- Encode variables ---
income = monthly_income
emp_self = 1 if employment_status == "Self Employed" else 0
emp_unemp = 1 if employment_status == "Unemployed" else 0
loan_home = 1 if loan_type == "Home" else 0
loan_personal = 1 if loan_type == "Personal" else 0
credit_good = 1 if credit_score == "Good" else 0
loc_urban = 1 if location == "Urban" else 0

# --- Logistic Regression Coefficients ---
intercept = 5.3551976259790495
coef_income = -0.0000259617687418
coef_emp_self = 1.6580628910103044
coef_emp_unemp = 4.4818219836163369
coef_loan_home = -2.4986504193573835
coef_loan_personal = 1.6928703494225534
coef_credit_good = -4.6784777493614556
coef_loc_urban = -1.5705748584574404

# --- Prediction Calculation ---
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

# --- Display output ---
if st.button("Predict Credit Risk"):
    st.markdown("<div class='output-container'>", unsafe_allow_html=True)
    if prob_default >= 0.5:
        st.markdown("<p class='output-text' style='color:#cc0000;'>RISKY</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p class='output-text' style='color:#009900;'>NOT RISKY</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
