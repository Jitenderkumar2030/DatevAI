import streamlit as st
from backend.auth_service import create_user

st.set_page_config(page_title="Sign Up - TallySmartAI")

st.title("📝 Create an Account")

email = st.text_input("Email")
pw = st.text_input("Password", type="password")
role = st.selectbox("Choose Role", ["free", "pro"])

if st.button("Sign up"):
    try:
        success = create_user(email, pw, role)
        if success:
            st.success("✅ Account created! Please [Login here](/Login)")
        else:
            st.error("❌ Signup failed.")
    except Exception as e:
        st.error(f"❌ Error: {e}")
