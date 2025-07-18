import streamlit as st

st.title("📞 Get in Touch")

st.markdown("Have questions? Reach out to us below:")

name = st.text_input("Your Name")
email = st.text_input("Your Email")
message = st.text_area("Your Message")

if st.button("Send Message"):
    st.success("✅ Message sent! We'll get back to you soon.")
