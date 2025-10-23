import streamlit as st
import numpy as np
from PIL import Image
import base64

# --------------------------
# 🏠 Page Setup
# --------------------------
st.set_page_config(page_title="NMIMS Loan Default Predictor", page_icon="💰", layout="centered")

# --------------------------
# 🖼️ Load Logo
# --------------------------
def get_base64_image(image_path):
    """Convert image to base64 for embedding."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

try:
    logo_base64 = get_base64_image("nmims-university-logo.png")
except FileNotFoundError:
    logo_base64 = None

# --------------------------
# 🎓 Fixed Header (Wide & Clean)
# --------------------------
header_html = f"""
    <style>
        [data-testid="stAppViewContainer"] {{
            padding-top: 130px !important;
        }}
        .fixed-header {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #ffffff;
            box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
            z-index: 1000;
            padding: 20px 0;
        }}
        .header-content {{
            max-width: 1000px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 50px;
        }}
        .header-title {{
            color: #800000;
            font-size: 4rem;
            font-weight: 900;
            margin: 0;
            letter-spacing: 0.5px;
        }}
        .header-logo {{
            width: 150px;
        }}
    </style>

    <div class="fixed-header">
        <div class="header-content">
            <p class="header-title">NMIMS Loan Default Risk Predictor</p>
            {"<img class='header-logo' src='data:image/png;base64," + logo_base64 + "'>" if logo_base64 else ""}
        </div>
    </div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# --------------------------
# 🧮 Input Section (Clean)
# --------------------------
st.markdown("<div style='max-width:700px; margin:auto;'>", unsafe_allow_html=True)
st.subheader("Enter Borrower Details")

income = st.text_input("Monthly Income (₹)", value="50000")
employment = st.selectbox("Employment Status", ["Salaried", "Self Employed"])
location = st.selectbox("Location", ["Urban", "Rural"])
loan_type = st.selectbox("Loan Type", ["Home", "Personal"])
rating = st.selectbox("Credit Rating", ["Good", "Bad"])

st.markdown("</div>", unsafe_allow_html=True)

# --------------------------
# 🧠 Logistic Regression Model
# --------------------------
try:
    income_val = float(income)
except:
    st.error("Please enter a valid numeric income value.")
    st.stop()

loan_val = 1 if loan_type == "Personal" else 0
emp_val = 1 if employment == "Self Employed" else 0
loc_val = 1 if location == "Urban" else 0
rating_val = 1 if rating == "Good" else 0

z = (
    7.80381648105447
    + (-1.17906553604e-05 * income_val)
    + (2.17358068940713 * loan_val)
    + (1.27679656359193 * emp_val)
    + (-2.44313166027285 * loc_val)
    + (-2.51690281035102 * rating_val)
)
prob_default = 1 / (1 + np.exp(-z))

# --------------------------
# 🎨 Predict Button
# --------------------------
st.markdown(
    """
    <style>
        .center-button {
            display: flex;
            justify-content: center;
            margin-top: 35px;
            margin-bottom: 60px;
        }
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #800000 0%, #b00000 100%);
            color: white;
            font-weight: 700;
            font-size: 22px;
            border-radius: 14px;
            padding: 1rem 2.5rem;
            border: none;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        div.stButton > button:first-child:hover {
            background: linear-gradient(135deg, #a00000 0%, #d00000 100%);
            transform: scale(1.05);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    predict_clicked = st.button("Predict Default Risk")

# --------------------------
# 📊 Prediction Result (Professional Minimal Output)
# --------------------------
if predict_clicked:
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<h3 style='text-align:center; color:#222;'>Predicted Probability of Default: <b>{prob_default * 100:.2f}%</b></h3>",
        unsafe_allow_html=True,
    )

    if prob_default >= 0.5:
        st.markdown(
            """
            <div style='text-align:center; color:#b00000; 
                        font-size:70px; font-weight:900; 
                        margin-top:2rem;'>
                ⚠️ RISKY
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div style='text-align:center; color:#007700; 
                        font-size:70px; font-weight:900; 
                        margin-top:2rem;'>
                ✅ NOT RISKY
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)
