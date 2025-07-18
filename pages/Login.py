import streamlit as st
import jwt

st.set_page_config(page_title="Login - TallySmartAI", layout="centered")

# Login Form
st.title("🔐 Login to TallySmartAI")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if email and password:
        role = "pro" if email.endswith("pro.com") else "free"

        token = jwt.encode({"email": email, "role": role}, "testsecret", algorithm="HS256")
        st.session_state["token"] = token
        st.session_state["logged_in"] = True

        # ✅ Navigate by URL or tell user to click Dashboard in sidebar
        st.success("✅ Login successful! Go to the Dashboard using the sidebar.")
        # OR: display a clickable link
        
    else:
        st.error("❌ Enter email and password.")
