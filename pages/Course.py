# pages/Course.py

import streamlit as st

st.set_page_config(page_title="TCFA Course Details - TallySmartAI", layout="wide")
st.title("📖 TCFA Course Curriculum & Registration")

st.markdown("""
## 📖 Course Curriculum

The **TCFA Program** includes the following modules:

1️⃣ Introduction to AI in Finance  
2️⃣ Tally Data Upload & Validation  
3️⃣ Financial Forecasting with TallySmartAI  
4️⃣ Using FinGPT for Business & Tax Q&A  
5️⃣ FinRL Smart Recommendations for Strategy  
6️⃣ Generating Professional Reports (PDF & Excel)  
7️⃣ Ensuring Data Security & Compliance  
8️⃣ Final Assessment & Certification

---

## 🗓️ Course Format

- 📅 Duration: 2 Weeks (Self-paced or Guided)  
- 🖥️ Mode: 100% Online  
- 📜 Assessment: Online test & practical project

---

## ✅ Registration Form

Fill the form below to express your interest. Our team will contact you for payment and further steps.

""")

name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number (Optional)")
experience = st.selectbox("Do you have experience with Tally?", ["Yes", "No"])
reason = st.text_area("Why do you want to join this course?")

if st.button("📨 Submit Registration"):
    if not name or not email:
        st.error("Please provide at least your name and email.")
    else:
        st.success(f"✅ Thank you, {name}! We will reach out to you at {email} soon.")
        # Optional: Integrate with your backend, email API, or Google Sheets here
