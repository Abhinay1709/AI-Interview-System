import streamlit as st
import os

from modules.resume_parser import extract_resume_text
from modules.skill_extractor import extract_skills

st.set_page_config(
    page_title="AI Interview Preparation System",
    page_icon="🎤",
    layout="wide"
)

st.title("🎤 AI Interview Preparation System")

st.write("Upload your resume to begin interview preparation.")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

if uploaded_file is not None:

    # Create uploads folder if not exists
    os.makedirs("uploads", exist_ok=True)

    # Save uploaded file
    file_path = os.path.join(
        "uploads",
        uploaded_file.name
    )

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ Resume Uploaded Successfully!")

    # Extract text
    resume_text = extract_resume_text(uploaded_file)

    # Display resume text
    st.subheader("📄 Extracted Resume Content")

    st.text_area(
        "Resume Text",
        resume_text,
        height=300
    )

    # Word count
    word_count = len(resume_text.split())

    # Extract skills
    skills = extract_skills(resume_text)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Resume Word Count",
            value=word_count
        )

    with col2:
        st.metric(
            label="Skills Detected",
            value=len(skills)
        )

    st.subheader("🛠 Detected Skills")

    if skills:
        for skill in skills:
            st.write(f"✅ {skill}")
    else:
        st.warning("No predefined skills detected.")

    st.subheader("📊 Resume Summary")

    st.info(
        f"""
        Total Words: {word_count}

        Skills Detected: {len(skills)}
        """
    )