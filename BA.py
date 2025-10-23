import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from PIL import Image

# --- App Configuration ---
st.set_page_config(page_title="Bank Analysis Dashboard", page_icon="🏦", layout="wide")

# --- Load Logo ---
try:
    logo = Image.open("nmims-university-logo.png")  # Make sure file is in same directory
    st.image(logo, width=200)
except Exception:
    st.warning("⚠️ Logo not found. Please ensure 'nmims-university-logo.png' is in the same folder.")

st.title("🏦 Bank Financial Health Dashboard")
st.markdown("A comprehensive financial analysis and default risk indicator dashboard.")

# --- File Upload Section ---
uploaded_file = st.file_uploader("📂 Upload your financial data (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File successfully uploaded!")
    st.dataframe(df.head())

    # --- Default Risk Calculation (Dummy Logic for Demo) ---
    # You can replace this with your own model/formula
    if "Debt" in df.columns and "Equity" in df.columns:
        debt_equity_ratio = (df["Debt"].sum() / df["Equity"].sum()) if df["Equity"].sum() != 0 else np.nan
    else:
        debt_equity_ratio = np.random.uniform(0.5, 3.0)  # fallback demo value

    if "CFO" in df.columns and "Interest" in df.columns:
        interest_cover = (df["CFO"].sum() / df["Interest"].sum()) if df["Interest"].sum() != 0 else np.nan
    else:
        interest_cover = np.random.uniform(0.5, 5.0)

    # Combine metrics into a simple risk score
    risk_score = (debt_equity_ratio / (interest_cover + 1)) * 10
    risk_score = np.clip(risk_score, 0, 10)

    st.subheader("📊 Financial Indicators")
    st.metric(label="Debt-to-Equity Ratio", value=f"{debt_equity_ratio:.2f}")
    st.metric(label="Interest Coverage Ratio", value=f"{interest_cover:.2f}")
    st.metric(label="Calculated Risk Score", value=f"{risk_score:.2f} / 10")

    # --- Semi-circle Risk Indicator ---
    st.subheader("🧭 Default Risk Indicator")

    color = "green" if risk_score < 5 else "red"
    risk_level = "Low Default Risk" if risk_score < 5 else "High Default Risk"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        number={'suffix': " / 10"},
        title={'text': risk_level, 'font': {'size': 20}},
        gauge={
            'axis': {'range': [0, 10], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': color, 'thickness': 0.3},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 5], 'color': 'lightgreen'},
                {'range': [5, 10], 'color': 'lightcoral'}
            ],
            'shape': "semi"
        }
    ))

    fig.update_layout(height=400, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("📄 Please upload a CSV file to begin analysis.")
