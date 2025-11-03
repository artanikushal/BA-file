import streamlit as st
import numpy as np

# --- Page Setup ---
st.set_page_config(page_title="Credit Risk Evaluation", layout="wide")

# --- Hide Streamlit’s default UI elements ---
hide_default_format = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
"""
st.markdown(hide_default_format, unsafe_allow_html=True)

# --- Custom CSS for design ---
st.markdown("""
<style>
    body {
        background-color: #f7f9fb;
        color: #222;
        font-family: "Segoe UI", sans-serif;
    }
    .main-header {
        text-align: center;
        background-color: white;
        padding: 30px 0 15px 0;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 50px;
    }
    .main-header h1 {
        font-size: 46px;
        font-weight: 800;
        color: #003366;
        letter-spacing: 1px;
    }
    .content {
        margin-top: 40px;
        padding: 0 80px;
    }
    .stSelectbox label, .stNumberInput label {
        font-weight: 600 !important;
        font-size: 17px !important;
        color: #003366 !important;
    }
    .stSelectbox, .stNumberInput {
        background: #ffffff;
        border-radius: 12px !important;
        padding: 10px 20px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    }
    .predict-btn {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 70px;
        margin-bottom: 40px;
    }
    .stButton > button {
        font-size: 24px !important;
        font-weight: 600;
        background-color: #2b7de9 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px;
        padding: 18px 80px;
        box-shadow: 0 4px 10px rgba(43,125,233,0.3);
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        background-color: #1a5fc1 !important;
        transform: scale(1.03);
    }
    .output-container {
        margin-top: 60px;
        text-align: center;
    }
    .output-text {
        font-size: 80px;
        font-weight: 900;
        text-align: center;
        margin-top: 30px;
        letter-spacing: 2px;
    }
    .prob-text {
        font-size: 32px;
        font-weight: 600;
        color: #333;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<div class='main-header'><h1>CREDIT RISK EVALUATION</h1></div>", unsafe_allow_html=True)

# --- Input Section ---
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

# --- Encode categorical values ---
income = monthly_income
emp_self = 1 if employment_status == "Self Employed" else 0
emp_unemp = 1 if employment_status == "Unemployed" else 0
loan_home = 1 if loan_type == "Home" else 0
loan_personal = 1 if loan_type == "Personal" else 0
credit_good = 1 if credit_score == "Good" else 0
loc_urban = 1 if location == "Urban" else 0

# --- Logistic regression coefficients ---
intercept = 5.3551976259790495
coef_income = -0.0000259617687418
coef_emp_self = 1.6580628910103044
coef_emp_unemp = 4.4818219836163369
coef_loan_home = -2.4986504193573835
coef_loan_personal = 1.6928703494225534
coef_credit_good = -4.6784777493614556
coef_loc_urban = -1.5705748584574404

# --- Logistic calculation ---
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

# --- Predict Button (centered) ---
st.markdown("<div class='predict-btn'>", unsafe_allow_html=True)
if st.button("Predict Credit Risk"):
    st.markdown("<div class='output-container'>", unsafe_allow_html=True)

    if prob_default >= 0.5:
        st.markdown("<p class='output-text' style='color:#cc0000;'>RISKY</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p class='output-text' style='color:#009900;'>NOT RISKY</p>", unsafe_allow_html=True)

    st.markdown(f"<p class='prob-text'>Default Probability: <b>{prob_default*100:.2f}%</b></p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
