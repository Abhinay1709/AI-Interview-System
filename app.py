import warnings

warnings.filterwarnings(
    "ignore",
    category=FutureWarning
)

# ----------------------------------
# Imports
# ----------------------------------

import streamlit as st
import os
import google.generativeai as genai

from config import GEMINI_API_KEY

from modules.resume_parser import extract_resume_text
from modules.skill_extractor import extract_skills
from modules.question_generator import generate_questions
from modules.speech_to_text import listen_and_convert
from modules.answer_evaluator import evaluate_answer
from modules.score_parser import extract_scores

from modules.database_manager import (
    create_table,
    save_interview,
    get_all_interviews,
    delete_interview,
    clear_database
)

from modules.report_generator import (
    generate_report
)

from modules.analytics import (
    calculate_statistics
)

from modules.export_history import (
    export_history
)

# ----------------------------------
# Gemini Configuration
# ----------------------------------

genai.configure(
    api_key=GEMINI_API_KEY
)

# ----------------------------------
# Database Initialization
# ----------------------------------

create_table()


# ----------------------------------
# Page Configuration
# ----------------------------------

st.set_page_config(
    page_title="AI Interview Preparation System",
    page_icon="🎤",
    layout="wide"
)

st.title("🎤 AI Interview Preparation System")

# ----------------------------------
# Sidebar
# ----------------------------------

st.sidebar.title(
    "Navigation"
)

st.sidebar.info(
    """
AI Interview Preparation System

Features:

✅ Resume Upload
✅ AI Questions
✅ Voice Answer
✅ AI Evaluation
✅ Database Storage
✅ Reports
✅ Analytics
"""
)

# ----------------------------------
# Session State Initialization
# ----------------------------------

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

# ----------------------------------
# Resume Upload Section
# ----------------------------------

st.header(
    "📄 Resume Upload"
)

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

# ----------------------------------
# Process Resume
# ----------------------------------

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
        "✅ Resume Uploaded Successfully!"
    )

    resume_text = extract_resume_text(
        uploaded_file
    )

    st.session_state.resume_text = (
        resume_text
    )

# ----------------------------------
# Resume Display Content
# ----------------------------------

    st.subheader(
        "📄 Extracted Resume Content"
    )

    st.text_area(
        "Resume Text",
        resume_text,
        height=250
    )

    # --------------------------
    # Skill Extraction
    # --------------------------

    skills = extract_skills(
        resume_text
    )

    word_count = len(
        resume_text.split()
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Resume Word Count",
            word_count
        )

    with col2:
        st.metric(
            "Skills Detected",
            len(skills)
        )

# ----------------------------------
# Display Skills
# ----------------------------------

    st.subheader(
        "🛠 Detected Skills"
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

# ----------------------------------
# Question Generation
# ----------------------------------

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

    elif not st.session_state.questions:

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

    else:

        st.info(
            "Questions already generated."
        )

# ----------------------------------
# Display Questions
# ----------------------------------

if st.session_state.questions:

    st.text_area(
        "Generated Questions",
        st.session_state.questions,
        height=300
    )

# ----------------------------------
# Reset Questions
# ----------------------------------

    if st.button(
        "🔄 Reset Questions"
    ):

        st.session_state.questions = ""

        st.rerun()

# ----------------------------------
# voice answer section
# ----------------------------------

st.divider()

st.header(
    "🎙 Answer Section"
)

# ----------------------------------
# Speech Recognition
# ----------------------------------

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

# ----------------------------------
# Manual Answer Input
# ----------------------------------

manual_answer = st.text_area(
    "Or Type Your Answer"
)

if manual_answer:

    st.session_state.current_answer = (
        manual_answer
    )

# ----------------------------------
# Display Current Answer
# ----------------------------------

if st.session_state.current_answer:

    st.subheader(
        "Your Answer"
    )

    st.text_area(
        "",
        st.session_state.current_answer,
        height=150
    )

# ----------------------------------
# AI Evaluation
# ----------------------------------

if st.session_state.current_answer:

    if st.button(
        "🤖 Evaluate Answer"
    ):

        if not st.session_state.evaluation:

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

        else:

            st.info(
                "Evaluation already generated."
            )

# ----------------------------------
# Evaluation Report
# ----------------------------------

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

# ----------------------------------
# Score Extraction & Dashboard
# ----------------------------------

    scores = extract_scores(
        st.session_state.evaluation
    )

    st.subheader(
        "📈 Performance Dashboard"
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

# ----------------------------------
# Overall Score
# ----------------------------------

    overall_score = round(
        (
            scores["technical"]
            + scores["communication"]
            + scores["confidence"]
        ) / 3,
        1
    )

    st.metric(
        "Overall Score",
        f"{overall_score}/10"
    )

    st.progress(
        min(
            int(overall_score * 10),
            100
        )
    )

    if st.button(
        "🔄 Reset Evaluation"
    ):

        st.session_state.evaluation = ""

        st.rerun()

# ----------------------------------
# Download Report
# ----------------------------------

report = generate_report(
    "Interview Question",
    st.session_state.current_answer,
    st.session_state.evaluation
)

st.download_button(
    label="📥 Download Report",
    data=report,
    file_name="interview_report.txt",
    mime="text/plain"
)

# ----------------------------------
# Save Interview To Database
# ----------------------------------

if st.session_state.current_answer:

    if st.button(
        "💾 Save Interview"
    ):

        save_interview(
            "Interview Question",
            st.session_state.current_answer,
            st.session_state.evaluation
        )

        st.success(
            "Interview Saved To Database!"
        )
        
# ----------------------------------
# Analytics Dashboard section
# ----------------------------------
st.divider()

st.header(
    "📈 Analytics Dashboard"
)

records = get_all_interviews()

stats = calculate_statistics(
    records
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Total Interviews",
        stats["total_interviews"]
    )

with col2:

    st.metric(
        "Average Technical Score",
        stats["average_score"]
    )

# ----------------------------------
# Download Full History
# ----------------------------------

history_report = export_history(
    records
)

st.download_button(
    label="📥 Download Full History",
    data=history_report,
    file_name="interview_history.txt",
    mime="text/plain"
)    

# ----------------------------------
# Clear Entire Database
# ----------------------------------

if st.button(
    "🗑 Clear Entire Database"
):
    clear_database()
    st.success(
        "Database Cleared Successfully!"
    )
    st.rerun()
    
# ----------------------------------
# Interview History
# ----------------------------------

st.divider()

st.header(
    "📚 Interview History"
)

records = get_all_interviews()

# ----------------------------------
# Display History
# ----------------------------------

if not records:

    st.info(
        "No interview records found."
    )

else:

    for record in records:

        record_id = record[0]

        question = record[1]

        answer = record[2]

        evaluation = record[3]

        # ----------------------------------
        # Expander
        # ----------------------------------

        with st.expander(
            f"Interview #{record_id}"
        ):

            st.write(
                "**Question:**"
            )

            st.write(
                question
            )

            st.write(
                "**Answer:**"
            )

            st.write(
                answer
            )

            st.write(
                "**Evaluation:**"
            )

            st.write(
                evaluation
            )

            # ----------------------------------
            # Delete Interview
            # ----------------------------------

            if st.button(
                f"🗑 Delete Interview {record_id}",
                key=f"delete_db_{record_id}"
            ):

                delete_interview(
                    record_id
                )

                st.success(
                    "Interview Deleted!"
                )

                st.rerun()

# ----------------------------------
# Footer
# ----------------------------------
st.divider()
st.caption(
    "🎤 AI Interview Preparation System | Final Year Project"
)