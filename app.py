import streamlit as st
import os
import google.generativeai as genai

from config import GEMINI_API_KEY

from modules.resume_parser import extract_resume_text
from modules.skill_extractor import extract_skills
from modules.question_generator import generate_questions
from modules.speech_to_text import listen_and_convert

from modules.answer_manager import (
    save_answer,
    delete_answer,
    clear_answers
)

from modules.answer_evaluator import evaluate_answer
from modules.score_parser import extract_scores

# -----------------------------
# Gemini Configuration
# -----------------------------

genai.configure(
    api_key=GEMINI_API_KEY
)

# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(
    page_title="AI Interview Preparation System",
    page_icon="🎤",
    layout="wide"
)

st.title("🎤 AI Interview Preparation System")

# -----------------------------
# Session State Initialization
# -----------------------------

if "responses" not in st.session_state:
    st.session_state.responses = []

if "questions" not in st.session_state:
    st.session_state.questions = ""

if "current_answer" not in st.session_state:
    st.session_state.current_answer = ""

if "evaluation" not in st.session_state:
    st.session_state.evaluation = ""

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

# -----------------------------
# Resume Upload Section
# -----------------------------

st.header("📄 Resume Upload")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

if uploaded_file is not None:

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    file_path = os.path.join(
        "uploads",
        uploaded_file.name
    )

    with open(file_path, "wb") as f:
        f.write(
            uploaded_file.getbuffer()
        )

    st.success(
        "Resume Uploaded Successfully!"
    )

    resume_text = extract_resume_text(
        uploaded_file
    )

    st.session_state.resume_text = (
        resume_text
    )

    st.subheader(
        "Extracted Resume Content"
    )

    st.text_area(
        "Resume Text",
        resume_text,
        height=250
    )

    # -----------------------------
    # Skills
    # -----------------------------

    skills = extract_skills(
        resume_text
    )

    word_count = len(
        resume_text.split()
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Word Count",
            word_count
        )

    with col2:
        st.metric(
            "Skills Detected",
            len(skills)
        )

    st.subheader(
        "Detected Skills"
    )

    if skills:

        for skill in skills:
            st.write(
                f"✅ {skill}"
            )

    else:

        st.warning(
            "No predefined skills detected."
        )

# -----------------------------
# Generate Questions
# -----------------------------

st.divider()

st.header(
    "🤖 AI Interview Questions"
)

if st.button(
    "Generate Interview Questions"
):

    if not st.session_state.resume_text:

        st.warning(
            "Please upload a resume first."
        )

    else:

        with st.spinner(
            "Generating Questions..."
        ):

            st.session_state.questions = (
                generate_questions(
                    st.session_state.resume_text
                )
            )

        st.success(
            "Questions Generated!"
        )

if st.session_state.questions:

    st.text_area(
        "Generated Questions",
        st.session_state.questions,
        height=300
    )

# -----------------------------
# Voice Answer Section
# -----------------------------

st.divider()

st.header(
    "🎙 Answer Section"
)

if st.button(
    "Start Recording"
):

    st.info(
        "Listening..."
    )

    answer = listen_and_convert()

    st.session_state.current_answer = (
        answer
    )

    st.success(
        "Speech Captured!"
    )

# -----------------------------
# Manual Input
# -----------------------------

manual_answer = st.text_area(
    "Or Type Your Answer"
)

if manual_answer:

    st.session_state.current_answer = (
        manual_answer
    )

# -----------------------------
# Display Answer
# -----------------------------

if st.session_state.current_answer:

    st.subheader(
        "Your Answer"
    )

    st.text_area(
        "",
        st.session_state.current_answer,
        height=150
    )

# -----------------------------
# AI Evaluation
# -----------------------------

if st.session_state.current_answer:

    if st.button(
        "🤖 Evaluate Answer"
    ):

        with st.spinner(
            "Evaluating..."
        ):

            st.session_state.evaluation = (
                evaluate_answer(
                    "Interview Question",
                    st.session_state.current_answer
                )
            )

        st.success(
            "Evaluation Completed!"
        )

# -----------------------------
# Evaluation Display
# -----------------------------

if st.session_state.evaluation:

    st.divider()

    st.header(
        "📊 AI Evaluation Report"
    )

    st.text_area(
        "Evaluation",
        st.session_state.evaluation,
        height=350
    )

    # -----------------------------
    # Score Dashboard
    # -----------------------------

    scores = extract_scores(
        st.session_state.evaluation
    )

    st.subheader(
        "Performance Dashboard"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Technical",
            f"{scores['technical']}/10"
        )

    with col2:
        st.metric(
            "Communication",
            f"{scores['communication']}/10"
        )

    with col3:
        st.metric(
            "Confidence",
            f"{scores['confidence']}/10"
        )

    overall_score = (
        scores["technical"]
        + scores["communication"]
        + scores["confidence"]
    ) / 3

    st.metric(
        "Overall Score",
        f"{round(overall_score,1)}/10"
    )

    st.progress(
        min(
            int(overall_score * 10),
            100
        )
    )

# -----------------------------
# Save Response
# -----------------------------

if st.session_state.current_answer:

    if st.button(
        "💾 Save Response"
    ):

        st.session_state.responses = (
            save_answer(
                "Interview Question",
                st.session_state.current_answer,
                st.session_state.evaluation,
                st.session_state.responses
            )
        )

        st.success(
            "Response Saved!"
        )

# -----------------------------
# Stored Responses
# -----------------------------

st.divider()

st.header(
    "📁 Stored Responses"
)

if len(
    st.session_state.responses
) == 0:

    st.info(
        "No responses saved yet."
    )

else:

    for index, response in enumerate(
        st.session_state.responses
    ):

        with st.expander(
            f"Response {index + 1}"
        ):

            st.write(
                "**Question:**"
            )
            st.write(
                response["question"]
            )

            st.write(
                "**Answer:**"
            )
            st.write(
                response["answer"]
            )

            st.write(
                "**Evaluation:**"
            )
            st.write(
                response["evaluation"]
            )

            if st.button(
                f"Delete Response {index+1}",
                key=f"delete_{index}"
            ):

                st.session_state.responses = (
                    delete_answer(
                        index,
                        st.session_state.responses
                    )
                )

                st.rerun()

# -----------------------------
# Clear All Responses
# -----------------------------

if len(
    st.session_state.responses
) > 0:

    if st.button(
        "🗑 Clear All Responses"
    ):

        st.session_state.responses = (
            clear_answers()
        )

        st.rerun()