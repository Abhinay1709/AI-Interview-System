# imports
import json
import streamlit as st
import os
import re
import google.generativeai as genai

from config import GEMINI_API_KEY

from modules.resume_parser import extract_resume_text
from modules.skill_extractor import extract_skills
from modules.question_generator import generate_questions

from modules.speech_to_text import listen_and_convert
from modules.answer_manager import clear_all_answers

from modules.answer_evaluator import evaluate_full_interview

from modules.database_manager import (
    create_table,
    save_interview,
    get_all_interviews,
    delete_interview,
    clear_database
)

from modules.report_generator import generate_full_report

from modules.analytics import calculate_statistics

from modules.export_history import export_history

from modules.score_parser import extract_scores

# Gemini configuration
genai.configure(
    api_key=GEMINI_API_KEY
)

# Database initialization
create_table()

# Page setup
st.set_page_config(
    page_title="AI Interview Preparation System",
    page_icon="🎤",
    layout="wide"
)

st.title(
    "🎤 AI Interview Preparation System"
)

# Sidebar navigation
st.sidebar.title(
    "Interview Progress"
)

# ── SESSION STATE ──────────────────────────────────────────────────────────────

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0

if "question_answers" not in st.session_state:
    st.session_state.question_answers = {}

if "final_evaluation" not in st.session_state:
    st.session_state.final_evaluation = ""

if "interview_completed" not in st.session_state:
    st.session_state.interview_completed = False

# NEW: True after "Save & Finish Interview" is clicked,
# but BEFORE evaluation runs
if "interview_finished" not in st.session_state:
    st.session_state.interview_finished = False

if "current_answer_text" not in st.session_state:
    st.session_state.current_answer_text = ""
    
# NEW: Track saving state for manual/auto save
if "is_saved" not in st.session_state:
    st.session_state.is_saved = False
    
if "auto_save" not in st.session_state:
    st.session_state.auto_save = True

# ── SIDEBAR SETTINGS ──────────────────────────────────────────────────────────

st.sidebar.divider()
st.session_state.auto_save = st.sidebar.toggle(
    "Auto-Save to History", 
    value=st.session_state.auto_save, 
    help="Automatically save the interview to the database after evaluation."
)


# ── RESUME UPLOAD ──────────────────────────────────────────────────────────────

st.header(
    "📄 Resume Upload"
)

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

if uploaded_file is not None:

    resume_text = extract_resume_text(uploaded_file)
    st.session_state.resume_text = resume_text

    st.success("Resume Uploaded Successfully")
    st.text_area("Resume Content", resume_text, height=200)

    skills = extract_skills(resume_text)
    st.subheader("Detected Skills")
    st.write(skills)

# ── GENERATE QUESTIONS ─────────────────────────────────────────────────────────

if st.button("Generate Interview Questions"):

    generated = generate_questions(
        st.session_state.resume_text
    )

    question_list = []
    for line in generated.split("\n"):
        line = line.strip()
        if line and line[0].isdigit():
            question_list.append(line)

    # Reset all interview state for a fresh start
    st.session_state.questions = question_list
    st.session_state.current_question_index = 0
    st.session_state.question_answers = {}
    st.session_state.interview_finished = False
    st.session_state.interview_completed = False
    st.session_state.final_evaluation = ""
    st.session_state.is_saved = False

    st.success(
        f"{len(question_list)} Questions Generated"
    )

# ── PROGRESS BAR (visible only while answering) ───────────────────────────────

if (
    st.session_state.questions
    and not st.session_state.interview_finished
):

    total_questions = len(st.session_state.questions)
    current = st.session_state.current_question_index + 1

    st.progress(current / total_questions)

    st.sidebar.metric(
        "Current Question",
        f"{current}/{total_questions}"
    )

# ── QUESTION / ANSWER / NAVIGATION ────────────────────────────────────────────

if (
    st.session_state.questions
    and not st.session_state.interview_finished
):

    question = st.session_state.questions[
        st.session_state.current_question_index
    ]

    existing_answer = st.session_state.question_answers.get(
        question, ""
    )

    total_questions = len(st.session_state.questions)

    is_last_question = (
        st.session_state.current_question_index
        == total_questions - 1
    )

    st.subheader(
        f"Question {st.session_state.current_question_index + 1}"
        f" of {total_questions}"
    )

    st.info(question)

    answer_text = st.text_area(
        "Your Answer",
        value=existing_answer,
        height=200,
        key=f"answer_{st.session_state.current_question_index}"
    )

    # Voice input
    if st.button("🎙 Record Answer"):
        voice_text = listen_and_convert()
        st.session_state.question_answers[question] = voice_text
        st.rerun()

    # Navigation buttons (Saving is handled within these actions)
    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Previous"):
            if st.session_state.current_question_index > 0:
                st.session_state.question_answers[question] = answer_text
                st.session_state.current_question_index -= 1
                st.rerun()

    with col2:
        if not is_last_question:
            # Questions 1 … N-1  →  "Save & Next"
            if st.button("➡ Save & Next"):
                st.session_state.question_answers[question] = answer_text
                st.session_state.current_question_index += 1
                st.rerun()
        else:
            # Last question  →  "Save & Finish Interview"
            if st.button(
                "🏁 Save & Finish Interview",
                type="primary"
            ):
                st.session_state.question_answers[question] = answer_text
                st.session_state.interview_finished = True
                st.rerun()

    # Sidebar answered count
    answered = len(st.session_state.question_answers)
    st.sidebar.metric("Answered", answered)

    # Warning for unanswered questions
    if answered < total_questions:
        st.warning(
            'Some questions are unanswered. '
            'Use "No" or "-" if you want to skip.'
        )

# ── EVALUATE SECTION ──────────────────────────────────────────────────────────
# Shown after "Save & Finish Interview" but before evaluation runs

if (
    st.session_state.interview_finished
    and not st.session_state.interview_completed
):

    st.header("🎯 Interview Finished!")
    st.success("All your answers have been saved locally for this session.")

    total = len(st.session_state.questions)
    answered = len(st.session_state.question_answers)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Questions", total)
    with col2:
        st.metric("Answers Recorded", answered)

    st.info(
        "Click **Evaluate Interview** to analyse all your answers "
        "and receive individual & overall scores."
    )

    if st.button("🔍 Evaluate Interview", type="primary"):

        with st.spinner("Evaluating your complete interview..."):
            evaluation = evaluate_full_interview(
                st.session_state.questions,
                st.session_state.question_answers
            )

        st.session_state.final_evaluation = evaluation
        st.session_state.interview_completed = True

        # Check if Auto-Save is enabled
        if st.session_state.auto_save:
            save_interview(
                st.session_state.questions,
                st.session_state.question_answers,
                evaluation
            )
            st.session_state.is_saved = True
            st.success("✅ Interview Evaluated & Auto-Saved!")
        else:
            st.success("✅ Interview Evaluated! (Auto-save is off. Manually save below if desired.)")
            
        st.rerun()

# ── EVALUATION REPORT ─────────────────────────────────────────────────────────

if st.session_state.interview_completed:

    st.header("📊 Final Interview Evaluation")

    st.text_area(
        "Evaluation",
        st.session_state.final_evaluation,
        height=350
    )
    
    st.divider()

    # ── Overall score dashboard
    scores = extract_scores(st.session_state.final_evaluation)

    st.subheader("📈 Overall Scores")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Technical", f"{scores['technical']}/10")
    with col2:
        st.metric("Communication", f"{scores['communication']}/10")
    with col3:
        st.metric("Confidence", f"{scores['confidence']}/10")
    with col4:
        st.metric("Overall", f"{scores['overall']}/10")

    st.divider()

    # ── Individual question scores
    question_scores = scores.get("question_scores", {})

    if question_scores:

        st.subheader("📝 Per-Question Scores")

        sorted_q_scores = sorted(
            question_scores.items(),
            key=lambda x: int(x[0].split()[-1])
        )

        # Display in rows of 5
        for row_start in range(0, len(sorted_q_scores), 5):
            row_items = sorted_q_scores[row_start : row_start + 5]
            q_cols = st.columns(len(row_items))
            for col_idx, (q_key, q_score) in enumerate(row_items):
                with q_cols[col_idx]:
                    st.metric(q_key, f"{q_score}/10")
        
        st.divider()

    # ── Actions: Download and Manual Save
    report = generate_full_report(
        st.session_state.questions,
        st.session_state.question_answers,
        st.session_state.final_evaluation
    )
    
    col_dl, col_save = st.columns(2)
    
    with col_dl:
        st.download_button(
            "📥 Download Report",
            report,
            file_name="Interview_Report.txt"
        )
        
    with col_save:
        if not st.session_state.is_saved:
            if st.button("💾 Save to History", type="primary"):
                save_interview(
                    st.session_state.questions,
                    st.session_state.question_answers,
                    st.session_state.final_evaluation
                )
                st.session_state.is_saved = True
                st.rerun()
        else:
            st.button("💾 Saved to History", disabled=True)

# ── ANALYTICS DASHBOARD ───────────────────────────────────────────────────────

records = get_all_interviews()
stats = calculate_statistics(records)

st.divider()
st.header("📈 Analytics Dashboard")

st.metric("Total Interviews", stats["total_interviews"])

st.divider()

# ── INTERVIEW HISTORY ─────────────────────────────────────────────────────────

st.header("📚 Interview History")

sorted_records = list(reversed(records))

for display_number, interview in enumerate(
    sorted_records, start=1
):

    if len(interview) < 5:
        continue

    interview_id    = interview[0]
    interview_date  = interview[1] or "Unknown Date"
    questions_raw   = interview[2]
    answers_raw     = interview[3]
    evaluation_text = interview[4]

    with st.expander(
        f"Interview #{display_number} — {interview_date}"
    ):

        try:
            # Handles 'null', empty strings safely avoiding JSON decoding errors on old records
            questions = json.loads(questions_raw) if questions_raw and questions_raw.strip() not in ['null', ''] else []
            answers   = json.loads(answers_raw)   if answers_raw and answers_raw.strip() not in ['null', ''] else {}
        except Exception:
            questions = []
            answers   = {}

        # Questions, Answers & Extracted Models
        if questions:

            st.subheader("📝 Questions, Answers & Feedback")

            for q_index, q_text in enumerate(questions, start=1):
                st.markdown(f"**Q{q_index}. {q_text}**")
                ans = answers.get(q_text, "*(No answer provided)*")
                st.write(f"**Your Answer:** {ans}")
                
                # Extract specific question score and model answer
                q_score = "N/A"
                model_answer = "*(Not available for this record)*"
                
                if evaluation_text:
                    score_match = re.search(rf"Question {q_index} Score:\s*(.*?/10)", evaluation_text, re.IGNORECASE)
                    if score_match:
                        q_score = score_match.group(1)
                        
                    model_match = re.search(rf"Question {q_index} Score:.*?Model Answer:\s*(.*?)(?=\nQuestion \d+ Score|\nTechnical Score|\nCommunication Score|\nQuestions Attempted|\Z)", evaluation_text, re.DOTALL | re.IGNORECASE)
                    if model_match:
                        model_answer = model_match.group(1).strip()
                
                # Display Score and Correct Answer cleanly
                st.info(f"**Score:** {q_score}\n\n**Correct/Model Answer:**\n{model_answer}")
                st.divider()

        else:
            st.info("No questions found for this record. (This may be an older database entry).")
            st.divider()

        # Evaluation text
        st.subheader("📊 Overall Evaluation")

        if evaluation_text:
            st.text(evaluation_text)
        else:
            st.info("No evaluation found for this record.")
            
        st.divider()

        # Scores summary inside history
        if evaluation_text:

            hist_scores = extract_scores(evaluation_text)
            tech = hist_scores.get("technical", 0)
            comm = hist_scores.get("communication", 0)
            conf = hist_scores.get("confidence", 0)
            ovrl = hist_scores.get("overall", 0)

            if tech > 0 or comm > 0 or conf > 0:

                st.subheader("📈 Scores")

                hc1, hc2, hc3, hc4 = st.columns(4)
                with hc1:
                    st.metric("Technical", f"{tech}/10")
                with hc2:
                    st.metric("Communication", f"{comm}/10")
                with hc3:
                    st.metric("Confidence", f"{conf}/10")
                with hc4:
                    st.metric("Overall", f"{ovrl}/10")
                    
                st.divider()

        # Download report from history
        report = generate_full_report(
            questions,
            answers,
            evaluation_text or "No evaluation available."
        )

        st.download_button(
            f"📥 Download Interview #{display_number}",
            report,
            file_name=f"Interview_{display_number}.txt",
            key=f"download_{interview_id}"
        )

        # Delete single interview
        if st.button(
            f"🗑 Delete Interview #{display_number}",
            key=f"delete_{interview_id}"
        ):
            delete_interview(interview_id)
            st.rerun()

# ── CLEAR ENTIRE HISTORY ──────────────────────────────────────────────────────
st.divider()
st.subheader("⚙️ Data Management")

col1, col2 = st.columns(2)

with col1:
    if st.button("🗑 Clear Entire History"):
        clear_database()
        st.success("All History Deleted")
        st.rerun()

with col2:
# ── EXPORT HISTORY ────────────────────────────────────────────────────────────
    if st.button("📤 Export All History"):
        history_report = export_history(records)
        st.download_button(
            "Download History Report",
            history_report,
            file_name="Interview_History.txt"
        )

# ── FOOTER ────────────────────────────────────────────────────────────────────

st.divider()
st.caption("AI Interview Preparation System v3.0")
st.markdown(
    """
    ---
    Developed by Abhinay Andhavarapu
    Powered by Google Gemini API
    """
)