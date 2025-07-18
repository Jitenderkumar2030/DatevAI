import streamlit as st
import jwt
import pandas as pd
import io
import os
from datetime import datetime
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# Backend imports
from backend.chat_advisor import get_financial_advice
from backend.telegram_alert import send_forecast_alert
from backend.cashfree import create_subscription_session

# AI modules
from ai_modules.fingpt_assistant import ask_fingpt
from ai_modules.finrl_agent import train_agent, get_finrl_recommendation

# --- UI & Auth ---
st.set_page_config(page_title="Dashboard - DatevAI", layout="wide")
st.title("📊 DatevAI Dashboard")

# Check session token
token = st.session_state.get("token")
if not token:
    st.warning("🔐 Please login to access the dashboard.")
    st.stop()

# Decode token
try:
    payload = jwt.decode(token, "testsecret", algorithms=["HS256"])
except:
    st.error("❌ Invalid or expired token.")
    st.session_state.clear()
    st.stop()

# Welcome and Logout
st.success(f"Welcome {payload['email']}! Role: `{payload['role']}`")

if st.button("🚪 Logout"):
    st.session_state.clear()
    st.success("Logged out successfully. Please refresh.")
    st.stop()

# --- Role-based access handling ---
if payload["role"] == "free":
    st.warning("🆓 You are using the Free Plan – Upgrade to Pro for full features!")

    # Show Upgrade to Pro before CSV upload
    if st.button("💳 Upgrade to Pro"):
        sub_url = create_subscription_session(payload["email"])
        if sub_url:
            st.markdown(f"[👉 Click here to Upgrade]({sub_url})", unsafe_allow_html=True)
        else:
            st.error("❌ Failed to generate payment link.")

# --- CSV Upload ---
st.subheader("📁 Upload Your Tally CSV")
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if not uploaded_file:
    st.info("📤 Please upload your Tally CSV to continue.")
    st.stop()

# Read uploaded CSV
df_uploaded = pd.read_csv(uploaded_file)
st.dataframe(df_uploaded.head())

# --- Free Plan Section ---
if payload["role"] == "free":
    st.markdown("### 🔍 Summary")
    st.metric("🔢 Total Transactions", len(df_uploaded))
    st.metric("💰 Total Revenue", f"₹ {df_uploaded['Amount'].sum():,.2f}")
    st.metric("🏆 Top Ledger", df_uploaded['Ledger'].value_counts().idxmax())

    # Revenue by Ledger Pie Chart
    st.subheader("🍰 Revenue by Ledger")
    ledger_totals = df_uploaded.groupby("Ledger")["Amount"].sum()
    st.pyplot(ledger_totals.plot.pie(autopct="%1.1f%%", figsize=(6, 6)).figure)

    # Monthly Revenue Trend
    try:
        df_uploaded["Date"] = pd.to_datetime(df_uploaded["Date"])
        monthly = df_uploaded.groupby(df_uploaded["Date"].dt.to_period("M"))["Amount"].sum().reset_index()
        monthly["Date"] = monthly["Date"].astype(str)
        st.subheader("📈 Monthly Revenue Trend")
        st.line_chart(monthly.set_index("Date")["Amount"])
    except:
        st.warning("⚠️ Could not generate monthly trend. Check your date format.")

# --- Pro/Admin Plan Section ---
if payload["role"] in ["pro", "admin"]:
    st.success("🎉 You have access to all Pro features!")

    # 1. Ask AI Advisor
    st.subheader("🧠 Ask an AI Financial Advisor")
    advisor_choice = st.radio("Select Advisor", ["DatevAI GPT Advisor", "FinGPT AI Analyst"])
    question = st.text_area("Ask a financial/business/tax question:")

    if st.button("Ask Advisor"):
        try:
            if advisor_choice == "DatevAI GPT Advisor":
                answer = get_financial_advice(question)
            else:
                answer = ask_fingpt(question)
            st.success(answer)
        except Exception as e:
            st.error(f"❌ AI error: {e}")

    # 2. Forecasting
    st.subheader("📈 AI Forecast Based on Uploaded CSV")
    try:
        files = {"file": uploaded_file.getvalue()}
        r = requests.post(
            "http://localhost:8000/predict",
            files=files,
            headers={"Authorization": f"Bearer {token}"}
        )

        if r.status_code == 200:
            forecast_df = pd.DataFrame(r.json())
            st.success("✅ Forecast Ready")
            st.dataframe(forecast_df)
            st.line_chart(forecast_df.set_index("ds")["yhat"])

            # CSV Download
            st.download_button("📥 Download CSV", forecast_df.to_csv(index=False), "forecast.csv")

            # Excel Download
            excel_io = io.BytesIO()
            with pd.ExcelWriter(excel_io, engine="xlsxwriter") as writer:
                forecast_df.to_excel(writer, index=False)
            st.download_button("📥 Download Excel", excel_io.getvalue(), "forecast.xlsx")

            # PDF Download
            pdf_io = io.BytesIO()
            c = canvas.Canvas(pdf_io, pagesize=letter)
            width, height = letter
            c.setFont("Helvetica-Bold", 14)
            c.drawString(30, height - 40, "📊 DatevAI - Forecast Report")
            c.setFont("Helvetica", 10)
            c.drawString(30, height - 60, f"Generated: {datetime.now()}")
            y = height - 90
            col_width = width / len(forecast_df.columns)
            for i, col in enumerate(forecast_df.columns):
                c.drawString(30 + i * col_width, y, str(col))
            y -= 20
            for row in forecast_df.head(20).values:
                for i, cell in enumerate(row):
                    c.drawString(30 + i * col_width, y, str(cell)[:15])
                y -= 15
                if y < 50:
                    c.showPage()
                    y = height - 50
            c.save()
            pdf_io.seek(0)
            st.download_button("📥 Download PDF", pdf_io, "forecast.pdf", "application/pdf")

            # Telegram Notification
            try:
                send_forecast_alert("your_telegram_user_id", "📊 Forecast completed in DatevAI.")
            except:
                st.warning("⚠️ Telegram alert failed.")
        else:
            st.error("❌ Forecast API failed.")
    except Exception as e:
        st.error(f"⚠️ Forecast Error: {e}")

    # 3. FinRL Smart Recommendation
    st.subheader("📊 FinRL Smart Recommendation")
    try:
        model = train_agent(df_uploaded)
        suggestion = get_finrl_recommendation(model, df_uploaded)
        st.success(f"📌 FinRL suggests: **{suggestion}** action for financial optimization.")
    except Exception as e:
        st.error(f"❌ FinRL error: {e}")
