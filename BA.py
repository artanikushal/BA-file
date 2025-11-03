import streamlit as st
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Credit Risk Evaluation", layout="wide")

# Hide Streamlit default UI
st.markdown("""
    <style>
        #MainMenu, header, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------------- CSS DESIGN ----------------
st.markdown("""
<style>
    body {
        background-color: #f8fafc;
        font-family: 'Segoe UI', sans-serif;
    }

    /* ===== Fixed Header ===== */
    .main-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        text-align: center;
        background-color: white;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        z-index: 999;
        padding: 25px 0 15px 0;
    }
    .main-header h1 {
        font-size: 52px;
        font-weight: 800;
        color: #003366;
        letter-spacing: 1px;
        margin: 0;
    }

    /* Add padding to top so content not hidden behind fixed header */
    .main-content {
        padding-top: 130px;
    }

    .stSelectbox label, .stNumberInput label {
        font-weight: 600 !important;
        color: #003366 !important;
        font-size: 17px !important;
    }

    div[data-baseweb="select"] > div {
        border-radius: 10px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
        background-color: white;
    }

    .stNumberInput > div > div > input {
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
    }

    /* ===== Predict Button ===== */
    .predict-btn {
        display: flex;
        justify-content: center;
        margin-top: 60px;
        margin-bottom: 40px;
    }
    .stButton > button {
        background: linear-gradient(90deg, #0066cc, #0099ff);
        color: white;
        font-size: 22px;
        font-weight: 600;
        padding: 18px 70px;
        border-radius: 12px;
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 10px rgba(0,102,204,0.3);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 15px rgba(0,102,204,0.35);
    }

    /* ===== Output ===== */
    .output-container {
        margin-top: 60px;
        text-align: center;
        justify-content: center
    }
    .output-text {
        font-size: 2000px;
        font-weight: 900;
        letter-spacing: 2px;
        margin-top: 20px;
    }
    .prob-text {
        font-size: 2000px;
        font-weight: 600;
        color: #222;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='main-header'><h1>CREDIT RISK EVALUATION</h1></div>", unsafe_allow_html=True)

# ---------------- MAIN CONTENT ----------------
st.markdown("<div class='main-content'>", unsafe_allow_html=True)

st.subheader("Enter Applicant Details")

col1, col2, col3 = st.columns(3)
with col1:
    employment_status = st.selectbox("Employment Status", ["Salaried", "Self Employed", "Unemployed"])
    loan_type = st.selectbox("Loan Type", ["Car", "Home", "Personal"])
with col2:
    credit_score = st.selectbox("Credit Score Rating", ["Good", "Bad"])
    location = st.selectbox("Location", ["Urban", "Rural"])
with col3:
    monthly_income = st.number_input("Monthly Income", min_value=1000, step=100, value=30000)

# ---------------- ENCODE INPUTS ----------------
income = monthly_income
emp_self = 1 if employment_status == "Self Employed" else 0
emp_unemp = 1 if employment_status == "Unemployed" else 0
loan_home = 1 if loan_type == "Home" else 0
loan_personal = 1 if loan_type == "Personal" else 0
credit_good = 1 if credit_score == "Good" else 0
loc_urban = 1 if location == "Urban" else 0

# ---------------- COEFFICIENTS ----------------
intercept = 5.3551976259790495
coef_income = -0.0000259617687418
coef_emp_self = 1.6580628910103044
coef_emp_unemp = 4.4818219836163369
coef_loan_home = -2.4986504193573835
coef_loan_personal = 1.6928703494225534
coef_credit_good = -4.6784777493614556
coef_loc_urban = -1.5705748584574404

# ---------------- PREDICTION ----------------
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

# ---------------- BUTTON ----------------
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
