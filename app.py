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

if "questions" not in st.session_state:
    st.session_state.questions = ""

if "question_list" not in st.session_state:
    st.session_state.question_list = []

if "selected_question" not in st.session_state:
    st.session_state.selected_question = ""

if "question_answers" not in st.session_state:
    st.session_state.question_answers = {}

if "question_evaluations" not in st.session_state:
    st.session_state.question_evaluations = {}

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

# ----------------------------------
# Resume Upload Section
# ----------------------------------

st.header(
    "📄 Resume Upload (PDF / DOCX)"
)

uploaded_file = st.file_uploader(
    "Upload Resume ",
    type=["pdf","docx"]
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

    else:

        with st.spinner(
            "Generating Questions..."
        ):

            generated_questions = generate_questions(
                st.session_state.resume_text
            )

            st.session_state.questions = (
                generated_questions
            )

            question_list = []

            for line in generated_questions.split("\n"):

                line = line.strip()

                if (
                    line
                    and line[0].isdigit()
                ):
                    question_list.append(
                        line
                    )

            st.session_state.question_list = (
                question_list
            )

        st.success(
            "Questions Generated!"
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
# Question selection
# ----------------------------------

if st.session_state.question_list:
    
    st.subheader(
        "📌 Select Question"
    )

    selected_question = st.selectbox(
        "Choose a question to answer",
        st.session_state.question_list
    )

    st.session_state.selected_question = (
        selected_question
    )

    st.info(
        f"Selected Question:\n\n{selected_question}"
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
    "🎙 Start Recording"
):

    if not st.session_state.selected_question:

        st.warning(
            "Please select a question first."
        )

    else:

        st.info(
            "Listening..."
        )

        spoken_text = listen_and_convert()

        selected_question = (
            st.session_state.selected_question
        )

        st.session_state.question_answers[
            selected_question
        ] = spoken_text

        st.success(
            "Speech Captured Successfully!"
        )

        st.success(
            "Speech Captured Successfully!"
        )

        st.rerun()

# ----------------------------------
# Question-wise Answer Section
# ----------------------------------

if st.session_state.selected_question:
    
    question = (
        st.session_state.selected_question
    )

    existing_answer = (
        st.session_state.question_answers.get(
            question,
            ""
        )
    )

    answer = st.text_area(

        f"Answer for:\n{question}",

        value=existing_answer,

        height=180,

        key=f"answer_{question}"
    )

    st.session_state.question_answers[
        question
    ] = answer

# ----------------------------------
# AI Evaluation
# ----------------------------------

if st.session_state.selected_question:

    if st.button(
        "🤖 Evaluate Answer"
    ):

        question = (
            st.session_state.selected_question
        )

        answer = (
            st.session_state.question_answers.get(
                question,
                ""
            )
        )

        if not answer.strip():

            st.warning(
                "Please enter an answer first."
            )

        else:

            with st.spinner(
                "Evaluating..."
            ):

                evaluation = evaluate_answer(
                    question,
                    answer
                )

            st.session_state.question_evaluations[
                question
            ] = evaluation

            st.success(
                "Evaluation Completed!"
            )


# ----------------------------------
# Evaluation Display
# ----------------------------------

question = (
    st.session_state.selected_question
)

evaluation = (
    st.session_state.question_evaluations.get(
        question,
        ""
    )
)

if evaluation:

    st.subheader(
        "📊 Evaluation Report"
    )

    st.text_area(
        "",
        evaluation,
        height=300
    )

# ----------------------------------
# Score Extraction & Dashboard
# ----------------------------------

    scores = extract_scores(
        evaluation
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
    question,
    st.session_state.question_answers.get(
        question,
        ""
    ),

    evaluation
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

if st.session_state.selected_question:

    if st.button(
        "💾 Save Interview"
    ):

        question = (
            st.session_state.selected_question
        )

        answer = (
            st.session_state.question_answers.get(
                question,
                ""
            )
        )

        evaluation = (
            st.session_state.question_evaluations.get(
                question,
                ""
            )
        )

        if not answer:

            st.error(
                "Please enter an answer first."
            )

        elif not evaluation:

            st.error(
                "Please evaluate the answer first."
            )

        else:

            save_interview(
                question,
                answer,
                evaluation
            )

            st.success(
                f"Saved: {question}"
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