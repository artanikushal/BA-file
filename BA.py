import streamlit as st
import numpy as np
from PIL import Image
import base64
from io import BytesIO

# --------------------------
# 🏠 Page Setup
# --------------------------
st.set_page_config(page_title="Loan Default Predictor", page_icon="💰", layout="centered")

# --------------------------
# 🎓 Load Local Logo and Encode for Fixed Header
# --------------------------
def get_base64_image(image_path):
    """Convert image to base64 to embed in HTML."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

try:
    logo_base64 = get_base64_image("nmims-university-logo.png")
except FileNotFoundError:
    logo_base64 = None

# --------------------------
# 🎓 Fixed Header (with local logo)
# --------------------------
header_html = f"""
    <style>
        [data-testid="stAppViewContainer"] {{
            padding-top: 160px !important; /* Space below fixed header */
        }}
        .fixed-header {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: white;
            box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
            z-index: 999;
            padding: 10px 0 5px 0;
        }}
        .header-content {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
        }}
        .header-title {{
            color: #800000;
            font-size: 1.9rem;
            font-weight: 700;
            margin: 0;
        }}
        .header-subtitle {{
            color: #555;
            font-size: 0.9rem;
            margin-top: 2px;
        }}
    </style>

    <div class="fixed-header">
        <div class="header-content">
            {"<img src='data:image/png;base64," + logo_base64 + "' width='70'>" if logo_base64 else ""}
            <div>
                <p class="header-title">NMIMS Loan Default Risk Predictor</p>
                <p class="header-subtitle">Predict borrower default likelihood using borrower details.</p>
            </div>
        </div>
    </div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# --------------------------
# 🧮 Input Section
# --------------------------
st.subheader("Enter Borrower Details")

income = st.text_input("Monthly Income (₹)", value="50000")
employment = st.selectbox("Employment Status", ["Salaried", "Self Employed"])
location = st.selectbox("Location", ["Urban", "Rural"])
loan_type = st.selectbox("Loan Type", ["Home", "Personal"])
rating = st.selectbox("Credit Rating", ["Good", "Bad"])

# --------------------------
# 🧠 Model Calculation (Full Precision)
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
# 🚀 Styled Predict Button
# --------------------------
st.markdown(
    """
    <style>
        div.stButton > button:first-child {
            background-color: #800000;
            color: white;
            font-weight: 600;
            font-size: 18px;
            border-radius: 12px;
            padding: 0.6rem 1.5rem;
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

st.markdown("---")

# --------------------------
# 🔍 Prediction Result
# --------------------------
if st.button("🔍 Predict Default Risk"):
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<h3 style='text-align:center; color:#444;'>Predicted Probability of Default: {prob_default * 100:.4f}%</h3>",
        unsafe_allow_html=True,
    )

    if prob_default >= 0.5:
        st.markdown(
            """
            <div style='text-align:center; background-color:#ffe6e6; color:red; 
                        font-size:58px; font-weight:700; border-radius:16px; 
                        padding:1rem; margin-top:1rem;'>
                ⚠️ RISKY
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div style='text-align:center; background-color:#e6ffe6; color:green; 
                        font-size:58px; font-weight:700; border-radius:16px; 
                        padding:1rem; margin-top:1rem;'>
                ✅ NOT RISKY
            </div>
            """,
            unsafe_allow_html=True,
        )
