# ==================================================
# IMPORTS
# ==================================================

import streamlit as st
import google.generativeai as genai
import re
import os

from config import *

from modules.resume_parser import (
    extract_resume_text,
    extract_resume_details,
    validate_resume
)

from modules.skill_extractor import (
    extract_skills,
    extract_skills_by_category
)

from modules.question_generator import (
    generate_questions
)

from modules.speech_to_text import (
    listen_and_convert,
    clean_speech_text
)

from modules.answer_manager import (
    get_answered_count,
    get_skipped_count,
    get_interview_statistics
)

from modules.answer_evaluator import (
    evaluate_full_interview
)

from modules.database_manager import (
    create_table,
    save_interview,
    get_all_interviews,
    delete_interview,
    clear_database,
    normalize_interview_record
)

from modules.report_generator import (
    generate_full_report
)

from modules.analytics import (
    calculate_statistics
)

from modules.export_history import (
    export_history_to_excel
)

from modules.score_parser import (
    extract_scores,
    get_question_score,
    get_model_answer,
    get_feedback
)

# ==================================================
# GEMINI CONFIGURATION
# ==================================================

genai.configure(
    api_key=GEMINI_API_KEY
)

# ==================================================
# DATABASE INITIALIZATION
# ==================================================

create_table()

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🎤",
    layout="wide"
)

# ==================================================
# TITLE
# ==================================================

st.title(
    "🎤 AI Interview Preparation System"
)

st.caption(
    f"Version {APP_VERSION}"
)

# ==================================================
# SESSION STATE
# ==================================================

default_states = {

    "resume_text": "",

    "resume_details": {},

    "skills": [],

    "projects": [],

    "questions": [],

    "current_question_index": 0,

    "question_answers": {},

    "final_evaluation": "",

    "interview_finished": False,

    "interview_completed": False,

    "auto_saved": False
}

for key, value in default_states.items():

    if key not in st.session_state:

        st.session_state[key] = value

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title(
    "Interview Progress"
)

# ==================================================
# RESUME UPLOAD
# ==================================================

st.header(
    "📄 Resume Upload"
)

uploaded_file = st.file_uploader(

    "Upload Resume",

    type=[
        "pdf",
        "docx",
        "txt"
    ]
)

# ==================================================
# PROCESS RESUME
# ==================================================

if uploaded_file is not None:
    st.write("File Name:", uploaded_file.name)
    st.write("File Type:", uploaded_file.type)
    st.write("File Size:", uploaded_file.size)
    resume_text = extract_resume_text(
        uploaded_file
    )
    
    st.write("Resume Text Length:", len(str(resume_text)))
    st.text_area(
        "Debug Resume Text",
        str(resume_text),
        height=200
    )

    if validate_resume(
        resume_text
    ):

        st.session_state.resume_text = (
            resume_text
        )

        resume_details = (
            extract_resume_details(
                resume_text
            )
        )

        st.session_state.resume_details = (
            resume_details
        )

        st.session_state.skills = (
            resume_details.get(
                "skills",
                []
            )
        )

        st.session_state.projects = (
            resume_details.get(
                "projects",
                []
            )
        )

        st.success(
            "Resume Parsed Successfully"
        )

        # ==========================================
        # CANDIDATE DETAILS
        # ==========================================

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"👤 Name: "
                f"{resume_details['name']}"
            )

            st.write(
                f"📧 Email: "
                f"{resume_details['email']}"
            )

        with col2:

            st.write(
                f"📱 Phone: "
                f"{resume_details['phone']}"
            )

        # ==========================================
        # RESUME CONTENT
        # ==========================================

        st.subheader(
            "Resume Content"
        )

        st.text_area(

            "Resume",

            resume_text,

            height=250
        )

        # ==========================================
        # DETECTED SKILLS
        # ==========================================

        st.subheader(
            "🛠 Detected Skills"
        )

        st.write(
            st.session_state.skills
        )

        categorized_skills = (
            extract_skills_by_category(
                resume_text
            )
        )

        for category, skill_list in (
            categorized_skills.items()
        ):

            with st.expander(
                category
            ):

                st.write(
                    skill_list
                )

        # ==========================================
        # DETECTED PROJECTS
        # ==========================================

        st.subheader(
            "📂 Detected Projects"
        )

        projects = (
            st.session_state.projects
        )

        if projects:

            for project in projects:

                st.write(
                    f"• {project}"
                )

        else:

            st.info(
                "No projects detected."
            )

    else:

        st.error(
            "Invalid Resume Uploaded"
        )

# ==================================================
# GENERATE QUESTIONS
# ==================================================

st.divider()

st.header(
    "🎯 Interview Questions"
)

if st.button(
    "Generate Questions",
    type="primary"
):

    if not st.session_state.resume_text:

        st.warning(
            "Upload Resume First"
        )

    else:

        with st.spinner(
            "Generating Questions..."
        ):

            question_list = (
                generate_questions(

                    st.session_state.resume_text,

                    st.session_state.skills,

                    st.session_state.projects
                )
            )

        st.session_state.questions = (
            question_list
        )

        st.session_state.current_question_index = 0

        st.session_state.question_answers = {}

        st.session_state.final_evaluation = ""

        st.session_state.interview_finished = False

        st.session_state.interview_completed = False

        st.session_state.auto_saved = False

        st.success(
            "10 Questions Generated Successfully"
        )

        st.rerun()

# ==================================================
# DISPLAY GENERATED QUESTIONS
# ==================================================

if st.session_state.questions:

    st.subheader(
        "Generated Questions"
    )

    for idx, question in enumerate(

        st.session_state.questions,

        start=1
    ):

        st.write(
            f"{idx}. {question}"
        )

# ==================================================
# INTERVIEW SECTION
# ==================================================

if (

    st.session_state.questions

    and

    not st.session_state.interview_finished

):

    st.divider()

    total_questions = len(
        st.session_state.questions
    )

    current_index = (
        st.session_state.current_question_index
    )

    current_question = (
        st.session_state.questions[
            current_index
        ]
    )

    # ==============================================
    # PROGRESS BAR
    # ==============================================

    progress = (
        (current_index + 1)
        /
        total_questions
    )

    st.progress(
        progress
    )

    st.sidebar.metric(
        "Current Question",
        f"{current_index + 1}/{total_questions}"
    )

    # ==============================================
    # LIVE COUNTS
    # ==============================================

    answered_count = (
        get_answered_count(
            st.session_state.question_answers
        )
    )

    skipped_count = (
        get_skipped_count(
            st.session_state.questions,
            st.session_state.question_answers
        )
    )

    st.sidebar.metric(
        "Answered",
        answered_count
    )

    st.sidebar.metric(
        "Skipped",
        skipped_count
    )

    # ==============================================
    # QUESTION HEADER
    # ==============================================

    st.subheader(
        f"Question {current_index + 1}"
        f" of {total_questions}"
    )

    st.info(
        current_question
    )

    # ==============================================
    # SKIP MESSAGE
    # ==============================================

    st.warning(
        """
If you don't know the answer, enter:

- No
- -
- N/A
- Skip

These answers will be treated as skipped questions.
"""
    )

    # ==============================================
    # EXISTING ANSWER
    # ==============================================

    existing_answer = (
        st.session_state.question_answers.get(
            current_question,
            ""
        )
    )

    answer_text = st.text_area(

        "Your Answer",

        value=existing_answer,

        height=220,

        key=f"answer_{current_index}"
    )

    # ==============================================
    # VOICE INPUT
    # ==============================================

    col_voice1, col_voice2 = (
        st.columns([1, 4])
    )

    with col_voice1:

        if st.button(
            "🎙 Record Answer"
        ):

            with st.spinner(
                "Listening..."
            ):

                voice_text = (
                    listen_and_convert()
                )

                voice_text = (
                    clean_speech_text(
                        voice_text
                    )
                )

                if voice_text:

                    st.session_state.question_answers[
                        current_question
                    ] = voice_text

                    st.success(
                        "Voice Answer Recorded"
                    )

                    st.rerun()

    # ==============================================
    # NAVIGATION
    # ==============================================

    st.divider()

    col1, col2 = st.columns(2)

    is_last_question = (

        current_index
        ==
        total_questions - 1
    )

    # ==============================================
    # PREVIOUS
    # ==============================================

    with col1:

        if st.button(
            "⬅ Previous"
        ):

            st.session_state.question_answers[
                current_question
            ] = answer_text

            if current_index > 0:

                st.session_state.current_question_index -= 1

                st.rerun()

    # ==============================================
    # NEXT / EVALUATE
    # ==============================================

    with col2:

        if not is_last_question:

            if st.button(
                "➡ Save & Next",
                type="primary"
            ):

                st.session_state.question_answers[
                    current_question
                ] = answer_text

                st.session_state.current_question_index += 1

                st.rerun()

        else:

            if st.button(
                "🎯 Generate Evaluation",
                type="primary"
            ):

                st.session_state.question_answers[
                    current_question
                ] = answer_text

                st.session_state.interview_finished = True

                st.rerun()

    # ==============================================
    # LIVE STATS
    # ==============================================

    st.divider()

    stats = (
        get_interview_statistics(

            st.session_state.questions,

            st.session_state.question_answers
        )
    )

    stat_col1, stat_col2, stat_col3 = (
        st.columns(3)
    )

    with stat_col1:

        st.metric(
            "Answered Questions",
            stats[
                "answered_questions"
            ]
        )

    with stat_col2:

        st.metric(
            "Skipped Questions",
            stats[
                "skipped_questions"
            ]
        )

    with stat_col3:

        st.metric(
            "Completion %",
            f"{stats['completion_percentage']}%"
        )
        
# ==================================================
# EVALUATION SCREEN
# ==================================================

if (

    st.session_state.interview_finished

    and

    not st.session_state.interview_completed

):

    st.divider()

    st.header(
        "🎯 Interview Completed"
    )

    stats = (
        get_interview_statistics(

            st.session_state.questions,

            st.session_state.question_answers
        )
    )

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    with col1:

        st.metric(
            "Total Questions",
            stats["total_questions"]
        )

    with col2:

        st.metric(
            "Answered",
            stats["answered_questions"]
        )

    with col3:

        st.metric(
            "Skipped",
            stats["skipped_questions"]
        )

    with col4:

        st.metric(
            "Completion %",
            f"{stats['completion_percentage']}%"
        )

    st.info(
        """
All answers have been recorded.

Click below to generate your
complete interview evaluation.
"""
    )

    if st.button(
        "🚀 Evaluate Interview",
        type="primary"
    ):

        with st.spinner(
            "Evaluating Interview..."
        ):

            evaluation = (
                evaluate_full_interview(

                    st.session_state.questions,

                    st.session_state.question_answers
                )
            )

        st.session_state.final_evaluation = (
            evaluation
        )

        st.session_state.interview_completed = True

        st.rerun()

# ==================================================
# DISPLAY EVALUATION
# ==================================================

if st.session_state.interview_completed:

    st.divider()

    st.header(
        "📊 Interview Evaluation"
    )

    evaluation_text = (
        st.session_state.final_evaluation
    )

    scores = (
        extract_scores(
            evaluation_text
        )
    )

    # ==============================================
    # AUTO SAVE
    # ==============================================

    if not st.session_state.auto_saved:

        save_interview(

            questions=(
                st.session_state.questions
            ),

            answers=(
                st.session_state.question_answers
            ),

            evaluation=(
                evaluation_text
            ),

            technical_score=(
                scores["technical"]
            ),

            communication_score=(
                scores["communication"]
            ),

            confidence_score=(
                scores["confidence"]
            ),

            overall_score=(
                scores["overall"]
            ),

            total_questions=(
                scores["total_questions"]
            ),

            answered_questions=(
                scores["attempted"]
            ),

            skipped_questions=(
                scores["skipped"]
            ),

            completion_percentage=(
                scores[
                    "completion_percentage"
                ]
            ),

            strengths=(
                scores["strengths"]
            ),

            weaknesses=(
                scores["weaknesses"]
            ),

            suggestions=(
                scores["suggestions"]
            )
        )

        st.session_state.auto_saved = True

        st.success(
            "Interview Automatically Saved"
        )

    # ==============================================
    # OVERALL SCORES
    # ==============================================

    st.subheader(
        "Overall Scores"
    )

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    with col1:

        st.metric(
            "Technical Score",
            f"{scores['technical']}/10"
        )

    with col2:

        st.metric(
            "Communication Score",
            f"{scores['communication']}/10"
        )

    with col3:

        st.metric(
            "Confidence Score",
            f"{scores['confidence']}/10"
        )

    with col4:

        st.metric(
            "Overall Score",
            f"{scores['overall']}/10"
        )

    # ==============================================
    # INTERVIEW STATS
    # ==============================================

    st.divider()

    stat1, stat2, stat3, stat4 = (
        st.columns(4)
    )

    with stat1:

        st.metric(
            "Total Questions",
            scores[
                "total_questions"
            ]
        )

    with stat2:

        st.metric(
            "Answered",
            scores[
                "attempted"
            ]
        )

    with stat3:

        st.metric(
            "Skipped",
            scores[
                "skipped"
            ]
        )

    with stat4:

        st.metric(
            "Completion %",
            f"{scores['completion_percentage']}%"
        )

    # ==============================================
    # QUESTION ANALYSIS
    # ==============================================

    st.divider()

    st.header(
        "📝 Question-wise Analysis"
    )

    for index, question in enumerate(

        st.session_state.questions,

        start=1
    ):

        answer = (
            st.session_state.question_answers.get(
                question,
                "No Answer"
            )
        )

        question_score = (
            get_question_score(
                evaluation_text,
                index
            )
        )

        model_answer = (
            get_model_answer(
                evaluation_text,
                index
            )
        )

        feedback = (
            get_feedback(
                evaluation_text,
                index
            )
        )

        with st.expander(
            f"Question {index}"
        ):

            st.markdown(
                f"### Question"
            )

            st.write(
                question
            )

            st.markdown(
                "### My Answer"
            )

            st.write(
                answer
            )

            st.markdown(
                "### Question Score"
            )

            st.metric(
                "Score",
                f"{question_score}/10"
            )

            st.markdown(
                "### Expected / Model Answer"
            )

            st.info(
                model_answer
            )

            st.markdown(
                "### Feedback"
            )

            st.warning(
                feedback
            )

    # ==============================================
    # STRENGTHS
    # ==============================================

    st.divider()

    st.subheader(
        "💪 Strengths"
    )

    st.success(
        scores["strengths"]
    )

    # ==============================================
    # WEAKNESSES
    # ==============================================

    st.subheader(
        "⚠ Weaknesses"
    )

    st.warning(
        scores["weaknesses"]
    )

    # ==============================================
    # SUGGESTIONS
    # ==============================================

    st.subheader(
        "📚 Suggestions"
    )

    st.info(
        scores["suggestions"]
    )

    # ==============================================
    # FULL EVALUATION
    # ==============================================

    with st.expander(
        "View Full Evaluation"
    ):

        st.text_area(

            "Evaluation",

            evaluation_text,

            height=500
        )

    # ==============================================
    # DOWNLOAD REPORT
    # ==============================================

    report = (
        generate_full_report(

            st.session_state.questions,

            st.session_state.question_answers,

            evaluation_text
        )
    )

    st.download_button(

        "📥 Download Report",

        report,

        file_name=(
            "Interview_Report.txt"
        ),

        mime="text/plain"
    )

# ==================================================
# ANALYTICS DASHBOARD
# ==================================================

st.divider()

st.header(
    "📈 Analytics Dashboard"
)

records = get_all_interviews()

stats = calculate_statistics(
    records
)

# ==============================================
# ROW 1
# ==============================================

col1, col2, col3, col4 = (
    st.columns(4)
)

with col1:

    st.metric(
        "Total Interviews",
        stats["total_interviews"]
    )

with col2:

    st.metric(
        "Avg Technical",
        f"{stats['average_technical']}/10"
    )

with col3:

    st.metric(
        "Avg Communication",
        f"{stats['average_communication']}/10"
    )

with col4:

    st.metric(
        "Avg Confidence",
        f"{stats['average_confidence']}/10"
    )

# ==============================================
# ROW 2
# ==============================================

col1, col2, col3, col4 = (
    st.columns(4)
)

with col1:

    st.metric(
        "Avg Overall",
        f"{stats['average_overall']}/10"
    )

with col2:

    st.metric(
        "Best Score",
        f"{stats['best_score']}/10"
    )

with col3:

    st.metric(
        "Worst Score",
        f"{stats['worst_score']}/10"
    )

with col4:

    st.metric(
        "Completion Rate",
        f"{stats['completion_rate']}%"
    )

# ==============================================
# ROW 3
# ==============================================

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Attempted Questions",
        stats["attempted_questions"]
    )

with col2:

    st.metric(
        "Skipped Questions",
        stats["skipped_questions"]
    )

# ==================================================
# INTERVIEW HISTORY
# ==================================================

st.divider()

st.header(
    "📚 Interview History"
)

if not records:

    st.info(
        "No interview history available."
    )

else:

    for interview_number, record in enumerate(

        records,

        start=1
    ):

        normalized = (
            normalize_interview_record(
                record
            )
        )

        interview_id = (
            normalized["id"]
        )

        interview_date = (
            normalized["date"]
        )

        questions = (
            normalized["questions"]
        )

        answers = (
            normalized["answers"]
        )

        evaluation_text = (
            normalized["evaluation"]
        )

        technical_score = (
            normalized[
                "technical_score"
            ]
        )

        communication_score = (
            normalized[
                "communication_score"
            ]
        )

        confidence_score = (
            normalized[
                "confidence_score"
            ]
        )

        overall_score = (
            normalized[
                "overall_score"
            ]
        )

        strengths = (
            normalized[
                "strengths"
            ]
        )

        weaknesses = (
            normalized[
                "weaknesses"
            ]
        )

        suggestions = (
            normalized[
                "suggestions"
            ]
        )

        with st.expander(

            f"Interview {interview_number}"

            f" | {interview_date}"

            f" | Overall: {overall_score}/10"

        ):

            # ==================================
            # SCORES
            # ==================================

            c1, c2, c3, c4 = (
                st.columns(4)
            )

            with c1:

                st.metric(
                    "Technical",
                    technical_score
                )

            with c2:

                st.metric(
                    "Communication",
                    communication_score
                )

            with c3:

                st.metric(
                    "Confidence",
                    confidence_score
                )

            with c4:

                st.metric(
                    "Overall",
                    overall_score
                )

            # ==================================
            # QUESTION ANALYSIS
            # ==================================

            st.subheader(
                "Question-wise Analysis"
            )

            for index, question in enumerate(

                questions,

                start=1
            ):

                answer = answers.get(
                    question,
                    "No Answer"
                )

                question_score = (
                    get_question_score(
                        evaluation_text,
                        index
                    )
                )

                model_answer = (
                    get_model_answer(
                        evaluation_text,
                        index
                    )
                )

                feedback = (
                    get_feedback(
                        evaluation_text,
                        index
                    )
                )

                with st.expander(
                    f"Question {index}"
                ):

                    st.markdown(
                        "### Question"
                    )

                    st.write(
                        question
                    )

                    st.markdown(
                        "### My Answer"
                    )

                    st.write(
                        answer
                    )

                    st.markdown(
                        "### Score"
                    )

                    st.metric(
                        "Question Score",
                        f"{question_score}/10"
                    )

                    st.markdown(
                        "### Model Answer"
                    )

                    st.info(
                        model_answer
                    )

                    st.markdown(
                        "### Feedback"
                    )

                    st.warning(
                        feedback
                    )

            # ==================================
            # STRENGTHS
            # ==================================

            st.subheader(
                "💪 Strengths"
            )

            st.success(
                strengths
            )

            # ==================================
            # WEAKNESSES
            # ==================================

            st.subheader(
                "⚠ Weaknesses"
            )

            st.warning(
                weaknesses
            )

            # ==================================
            # SUGGESTIONS
            # ==================================

            st.subheader(
                "📚 Suggestions"
            )

            st.info(
                suggestions
            )

            # ==================================
            # FULL EVALUATION
            # ==================================

            with st.expander(
                "View Full Evaluation"
            ):

                st.text_area(

                    "Evaluation",

                    str(
                        evaluation_text
                    ),

                    height=400,

                    key=f"eval_"
                        f"{interview_id}"
                )

            # ==================================
            # DOWNLOAD OLD REPORT
            # ==================================

            report = (
                generate_full_report(

                    questions,

                    answers,

                    evaluation_text
                )
            )

            st.download_button(

                label=(
                    f"📥 Download Report"
                ),

                data=report,

                file_name=(

                    f"Interview_"

                    f"{interview_id}"

                    f".txt"
                ),

                mime="text/plain",

                key=(
                    f"download_"
                    f"{interview_id}"
                )
            )

            # ==================================
            # DELETE INTERVIEW
            # ==================================

            if st.button(

                f"🗑 Delete Interview",

                key=(
                    f"delete_"
                    f"{interview_id}"
                )
            ):

                delete_interview(
                    interview_id
                )

                st.success(
                    "Interview Deleted"
                )

                st.rerun()
                
# ==================================================
# EXPORT HISTORY
# ==================================================

st.divider()

st.header(
    "📤 Export Interview History"
)

if records:

    col1, col2 = st.columns(2)

    # ==============================================
    # GENERATE EXCEL
    # ==============================================

    with col1:

        if st.button(
            "📊 Generate Excel Export"
        ):

            excel_file = (
                export_history_to_excel(
                    records
                )
            )

            st.session_state[
                "excel_file"
            ] = excel_file

            st.success(
                "Excel File Generated"
            )

    # ==============================================
    # DOWNLOAD EXCEL
    # ==============================================

    with col2:

        if (
            "excel_file"
            in st.session_state
        ):

            try:

                with open(

                    st.session_state[
                        "excel_file"
                    ],

                    "rb"
                ) as file:

                    st.download_button(

                        label=(
                            "📥 Download Excel"
                        ),

                        data=file,

                        file_name=(
                            "Interview_History.xlsx"
                        ),

                        mime=(

                            "application/"

                            "vnd.openxmlformats-"

                            "officedocument."

                            "spreadsheetml.sheet"
                        )
                    )

            except Exception:

                st.warning(
                    "Generate Excel file first."
                )

else:

    st.info(
        "No interview history available for export."
    )

# ==================================================
# HISTORY MANAGEMENT
# ==================================================

st.divider()

st.header(
    "⚠ History Management"
)

if records:

    st.warning(
        """
This will permanently delete all
interview history and reports.
"""
    )

    if st.button(
        "🗑 Delete Entire History"
    ):

        clear_database()

        st.success(
            "Entire Interview History Deleted"
        )

        # ==========================
        # RESET CURRENT SESSION
        # ==========================

        st.session_state.questions = []

        st.session_state.question_answers = {}

        st.session_state.final_evaluation = ""

        st.session_state.interview_finished = False

        st.session_state.interview_completed = False

        st.session_state.auto_saved = False

        st.rerun()

else:

    st.info(
        "No interview history available."
    )

# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "🎤 AI Interview Preparation System"
)

st.caption(
    f"Version {APP_VERSION}"
)

st.markdown(
    """
---

## Features

✅ Resume Upload (PDF / DOCX / TXT)

✅ Resume Parsing

✅ Candidate Details Extraction

✅ Skill Detection

✅ Project Detection

✅ AI-Based Question Generation

✅ 5 Technical Questions

✅ 3 HR Questions

✅ 2 Project Questions

✅ Voice Input Support

✅ One Question At A Time

✅ Previous / Save & Next

✅ Skip Question Handling

✅ Question-wise Evaluation

✅ Model Answers

✅ Feedback Generation

✅ Technical Score

✅ Communication Score

✅ Confidence Score

✅ Overall Score

✅ Completion Percentage

✅ Auto Save Interview

✅ Download Report

✅ Analytics Dashboard

✅ Interview History

✅ Download Old Reports

✅ Delete Individual Interview

✅ Delete Entire History

✅ Export History To Excel

"""
)

# ==================================================
# END OF APP
# ==================================================