import streamlit as st
from backend.models import SessionLocal, User
from backend.auth import hash_password

st.title("🔁 Reset Password")

email = st.text_input("Registered Email")
new_pw = st.text_input("New Password", type="password")

if st.button("Reset Password"):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.password = hash_password(new_pw)
        db.commit()
        st.success("✅ Password updated successfully.")
    else:
        st.error("❌ Email not found.")
    db.close()
