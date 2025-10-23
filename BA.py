import streamlit as st
import numpy as np
from PIL import Image
import base64

# --------------------------
# 🏠 Page Setup
# --------------------------
st.set_page_config(page_title="NMIMS Loan Default Predictor", page_icon="💰", layout="centered")

# --------------------------
# 🖼️ Load Local Logo
# --------------------------
def get_base64_image(image_path):
    """Convert image to base64 for embedding in header."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

try:
    logo_base64 = get_base64_image("nmims-university-logo.png")
except FileNotFoundError:
    logo_base64 = None

# --------------------------
# 🎓 Fixed Header (Big Title + Wide Layout)
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
            background-color: white;
            box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
            z-index: 1000;
            padding: 18px 0;
        }}
        .header-content {{
            max-width: 1000px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 40px;
        }}
        .header-title {{
            color: #800000;
            font-size: 3.8rem;
            font-weight: 900;
            margin: 0;
            letter-spacing: 0.5px;
        }}
        .header-logo {{
            width: 130px;
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
# 🧮 Input Section (Centered & Clean)
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
# 🎨 Predict Button (Centered)
# --------------------------
st.markdown(
    """
    <style>
        .center-button {
            display: flex;
            justify-content: center;
            margin-top: 35px;
            margin-bottom: 50px;
        }
        div.stButton > button:first-child {
            background-color: #800000;
            color: white;
            font-weight: 600;
            font-size: 22px;
            border-radius: 12px;
            padding: 0.9rem 2.5rem;
            border: none;
            transition: all 0.3s ease;
        }
        div.stButton > button:first-child:hover {
            background-color: #a00000;
            transform: scale(1.05);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    predict_clicked = st.button("🔍 Predict Default Risk")

# --------------------------
# 📊 Prediction Result (Big Text, Centered)
# --------------------------
if predict_clicked:
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<h3 style='text-align:center; color:#333;'>Predicted Probability of Default: {prob_default * 100:.4f}%</h3>",
        unsafe_allow_html=True,
    )

    if prob_default >= 0.5:
        st.markdown(
            """
            <div style='text-align:center; background-color:#ffe6e6; color:red; 
                        font-size:70px; font-weight:900; border-radius:20px; 
                        padding:1.5rem; margin-top:1.5rem;'>
                ⚠️ RISKY
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div style='text-align:center; background-color:#e6ffe6; color:green; 
                        font-size:70px; font-weight:900; border-radius:20px; 
                        padding:1.5rem; margin-top:1.5rem;'>
                ✅ NOT RISKY
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)
