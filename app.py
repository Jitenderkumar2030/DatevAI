# app.py (main Streamlit app)

import streamlit as st

st.set_page_config(page_title="DatevAI", page_icon="📊", layout="wide")

# Optional Redirect Handler
page = st.session_state.get("page")
if page == "login":
    st.session_state["page"] = None
    st.switch_page("pages/Login.py")
elif page == "dashboard":
    st.session_state["page"] = None
    st.switch_page("pages/Dashboard.py")

# Sidebar
with st.sidebar:
    st.title("🧭 DatevAI Academy")
    st.markdown("Navigate using the sidebar or use buttons below 👇")
    if st.button("📚 DCFA Certification"):
        st.switch_page("pages/Certification.py")

    if st.button("🎓 DCFA Course"):
        st.switch_page("pages/Course.py")

# Landing Page
st.title("📊 Welcome to DatevAI")

st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://images.pexels.com/photos/7876971/pexels-photo-7876971.jpeg" style="width: 800px; height: auto;">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""  
### AI-Powered Forecasting & Financial Advisory Platform  
> Upload DATEV CSV. Get instant forecasts, financial insights, and downloadable reports.  
""")

# Login / Signup Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🔐 Login", use_container_width=True):
        st.session_state["page"] = "login"
        st.rerun()
with col2:
    if st.button("📝 Signup", use_container_width=True):
        st.session_state["page"] = "signup"
        st.switch_page("pages/Signup.py")

# Features
st.markdown("### 🔍 Explore More")

col_feat, col_review = st.columns(2)

with col_feat:
    st.subheader("🚀 Why DatevAI?")
    st.markdown("""
- 📈 **Instant Financial Forecasting**  
- 🤖 **AI-powered Business Insights**  
- 📄 **Auto-generated Reports & Trend Analysis**  
- 🔐 **End-to-End Data Security**  
- 🌐 **Access Anywhere, Anytime**  
- 🧠 **FinGPT AI Analyst** — Ask finance, business, or tax questions to an advanced language model  
- 🧮 **FinRL Smart Recommendation Engine** — Reinforcement Learning engine to suggest strategic financial actions
    """)

with col_review:
    st.subheader("💬 What Our Users Say")
    st.success("“DatevAI saved us hours of manual effort each week. The insights are spot on!” – Priya, CFO at RetailNest")
    st.info("“Seamless integration and excellent support. Game-changer for small businesses.” – Rohan, Founder of GreenMart")
    st.warning("“Loved the reports and visual insights. Helped us make faster decisions.” – Meena, Head of Finance at FinBridge")

# Certification / Course Section
st.markdown("---")
st.header("🎓 DatevAI Certified Financial Analyst Program (DCFA)")

st.markdown("""
Become a **DatevAI Certified Financial Analyst (DCFA)** and master AI-powered accounting, forecasting, and analytics.

✅ What you’ll learn:
- Upload & manage Datev data effectively  
- Use AI forecasting & FinRL recommendations  
- Get answers from FinGPT for business/tax queries  
- Generate insightful PDF/Excel reports  
- Securely handle financial data

💼 **Ideal for** accountants, business owners, finance students, and professionals looking to boost their skills.

💰 **Course Fees:** INR 2,999 – 4,999 per participant

📜 **Certification:** Receive an industry-recognized certificate upon successful completion.

[👉 Enroll in DCFA Now](https://your-enrollment-form-or-payment-link.com)
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 10px; font-size: 14px;'>
    © 2025 <strong>DatevAI</strong> | Built with ❤️ by Jitender Kumar  
    <br>Need help? <a href="/7_Contact_Us" target="_self">📞 Contact Support</a>
</div>
""", unsafe_allow_html=True)
