import streamlit as st

st.set_page_config(
    page_title="AI Interview System",
    page_icon="🎤",
    layout="centered"
)

st.title("🎤 AI Interview Preparation System")

st.write("Welcome to the AI-powered mock interview platform.")

if st.button("Start Interview"):
    st.success("System Ready!")