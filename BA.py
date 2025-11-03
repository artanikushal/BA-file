import streamlit as st
import joblib
import numpy as np
from PIL import Image

# Load your trained model
model = joblib.load("model.pkl")  # Ensure model.pkl is in the same folder

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
        padding: 20px 0;
        border-bottom: 2px solid #eee;
        position: fixed;
        top: 0;
        width: 100%;
        z-index: 999;
    }
    .main-header img {
        height: 80px;
        margin-right: 20px;
    }
    .main-header h1 {
        font-size: 36px;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin: 0;
    }
    .content {
        margin-top: 160px;
        padding: 20px;
    }
    .stButton > button {
        display: block;
        margin: 30px auto;
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
        font-size: 28px;
        font-weight: bold;
        margin-top: 30px;
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

# Upload logo or image section
uploaded
