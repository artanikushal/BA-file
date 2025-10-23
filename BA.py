import streamlit as st
import numpy as np
from PIL import Image
import base64

# --------------------------
# 🏠 Page Setup
# --------------------------
st.set_page_config(page_title="Loan Default Predictor", page_icon="💰", layout="centered")

# --------------------------
# 🎓 Load Local Logo and Encode
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
# 🎓 Fixed Header (larger and cleaner)
# --------------------------
header_html = f"""
    <style>
        [data-testid="stAppViewContainer"] {{
            padding-top: 200px !important; /* Space for header */
        }}
        .fixed-header {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: white;
            box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
            z-index: 999;
            padding: 18px 0 12px 0;
        }}
        .header-content {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 18px;
        }}
        .header-title {{
            color: #800000;
            font-size: 2.3rem;
            font-weight: 800;
            margin: 0;
        }}
        .header-subtitle {{
            color: #555;
            font-size: 1rem;
            margin-top: 4px;
        }}
    </style>

    <div class="fixed-header">
        <div class="header-content">
            {"<img src='data:image/png;base64," + logo_base64 + "' width='90'>" if logo_base64 else ""}
            <div>
                <p class="header-title">NMIMS Loan Default Risk Predictor</p>
                <p class="header-subtitle">Predict the likelihood of borrower default based on key details.</p>
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

# full precision coefficients
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
# 🎨 Center-Aligned Predict Button
# --------------------------
st.markdown(
    """
    <style>
        .center-button {
            display: flex;
            justify-content: center;
            margin-top: 30px;
        }
        div.stButton > button:first-child {
            background-color: #800000;
            color: white;
            font-weight: 600;
            font-size: 20px;
            border-radius: 12px;
            padding: 0.8rem 2rem;
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

# Create a center container for the button
button_placeholder = st.container()
with button_placeholder:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        predict_clicked = st.button("🔍 Predict Default Risk")

# --------------------------
# 📊 Prediction Result
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
                        font-size:60px; font-weight:800; border-radius:18px; 
                        padding:1.2rem; margin-top:1.5rem;'>
                ⚠️ RISKY
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div style='text-align:center; background-color:#e6ffe6; color:green; 
                        font-size:60px; font-weight:800; border-radius:18px; 
                        padding:1.2rem; margin-top:1.5rem;'>
                ✅ NOT RISKY
            </div>
            """,
            unsafe_allow_html=True,
        )

    # add space at bottom
    st.markdown("<div style='height:120px;'></div>", unsafe_allow_html=True)
