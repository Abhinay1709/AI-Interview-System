# ==================================================
# PART 1: MAIN APPLICATION
# ==================================================
# IMPORTS
# ==================================================

import streamlit as st

import pandas as pd
import google.generativeai as genai
import re
import os

from config import *

from modules.ats_analyzer import calculate_ats_score

from modules.resume_insights import generate_resume_insights

from modules.resume_parser import (
    extract_resume_text,
    extract_resume_details,
    validate_resume
)

from modules.skill_extractor import (
    extract_skills,
    extract_skills_by_category
)

from modules.question_generator import generate_questions
from modules.speech_to_text import listen_and_convert, clean_speech_text
from modules.answer_manager import get_answered_count, get_skipped_count, get_interview_statistics
from modules.answer_evaluator import evaluate_full_interview
from modules.database_manager import (
    create_table,
    save_interview,
    get_all_interviews,
    delete_interview,
    clear_database,
    normalize_interview_record
)
from modules.report_generator import generate_full_report
from modules.analytics import calculate_statistics
from modules.skill_gap_analyzer import (
    analyze_skill_gap
)
from modules.export_history import export_history_to_excel
from modules.score_parser import (
    extract_scores,
    get_question_score,
    get_model_answer,
    get_feedback
)

from modules.charts import (
    create_radar_chart,
    create_score_trend_chart,
    create_skill_trend_chart
)

from modules.dashboard import (
    calculate_readiness,
    show_dashboard_metrics,
    show_resume_summary,
    show_candidate_details,
    show_system_status,
    show_placement_summary,
    show_interview_tracker
)

from modules.profile_card import (
    show_profile_card,
    show_readiness_card
)

from modules.recommendation_engine import (
    calculate_role_matches,
    calculate_resume_match
)

from modules.candidate_intelligence import (
    calculate_placement_probability,
    get_best_career_path,
    get_learning_roadmap
)

from modules.advanced_analytics import (
    calculate_improvement,
    calculate_consistency,
    strongest_area,
    weakest_area
)

from page_modules.dashboard_page import show_dashboard_page
from page_modules.resume_page import show_resume_page
from page_modules.interview_page import show_interview_page
from page_modules.evaluation_page import show_evaluation_page
from page_modules.analytics_page import show_analytics_page
from page_modules.history_page import show_history_page# ==================================================
# GEMINI CONFIGURATION
# ==================================================

genai.configure(api_key=GEMINI_API_KEY)

# ==================================================
# DATABASE INITIALIZATION
# ==================================================

create_table()

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
<style>
/* Main Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b, #111827);
}
/* Main Headers */
h1 {
    text-align: center;
    font-size: 3rem !important;
    font-weight: 800 !important;
    color: #38bdf8 !important;
}
h2, h3 {
    color: white !important;
}
/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: 1px solid #334155;
}
/* Metric Cards */
div[data-testid="metric-container"] {
    background: #1e293b;
    border-radius: 15px;
    padding: 15px;
    border: 1px solid #334155;
}
/* Buttons */
.stButton button {
    width: 100%;
    border-radius: 12px;
    font-weight: 600;
}
/* File Uploader */
[data-testid="stFileUploader"] {
    border: 2px dashed #38bdf8;
    border-radius: 15px;
    padding: 15px;
}
/* Text Areas */
textarea {
    border-radius: 12px !important;
}
/* Progress Bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #06b6d4, #2563eb);
}
</style>
""",
    unsafe_allow_html=True
)

# ==================================================
# TITLE
# ==================================================

st.markdown(
    """
<div style='text-align:center;padding:20px'>
    <h1>🚀 AI Interview Coach</h1>
    <p style='font-size:18px;color:#cbd5e1'>
        Resume Analysis • Smart Questions • AI Evaluation
    </p>
</div>
""",
    unsafe_allow_html=True
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
    "last_resume": "",
    "show_evaluation_button": False,
    "job_role": "AI Engineer",
    "current_question_index": 0,
    "question_answers": {},
    "final_evaluation": "",
    "interview_finished": False,
    "interview_completed": False,
    "auto_saved": False,
    "difficulty": "Intermediate",
    "ats_score": 0
}

for key, value in default_states.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.markdown(
    """
    <div style="
        text-align:center;
        padding:15px;
        border-radius:15px;
        background:#1e293b;
        border:1px solid #334155;
        margin-bottom:15px;
    ">

    <h2 style="color:white;">
        🚀 AI Interview Coach
    </h2>

    <p style="color:#cbd5e1;">
        AI Powered Mock Interview Platform
    </p>

    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")


page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📄 Resume Analysis",
        "🎯 Interview",
        "📊 Evaluation",
        "📈 Analytics",
        "📚 History"
    ],
    index=[
        "🏠 Dashboard",
        "📄 Resume Analysis",
        "🎯 Interview",
        "📊 Evaluation",
        "📈 Analytics",
        "📚 History"
    ].index(
        st.session_state.get(
            "current_page",
            "📄 Resume Analysis"
        )
    )
)
st.session_state.current_page = page

st.sidebar.markdown("---")
st.sidebar.markdown("### 🚀 Workflow")

workflow_steps = [
    ("📄 Resume Upload",
     bool(st.session_state.resume_text)),
    ("🛠 Skill Detection",
     len(st.session_state.skills) > 0),
    ("❓ Question Generation",
     len(st.session_state.questions) > 0),
    ("🎤 Interview Practice",
     st.session_state.interview_finished),
    ("📊 Evaluation",
     st.session_state.interview_completed),
    ("📈 Analytics",
     True),
    ("📥 Report Download",
     st.session_state.interview_completed)

]
for step, completed in workflow_steps:
    if completed:
        st.sidebar.success(step)
    else:
        st.sidebar.info(step)



if page == "🏠 Dashboard":
    show_dashboard_page()

elif page == "📄 Resume Analysis":
    show_resume_page()

elif page == "🎯 Interview":
    show_interview_page()

elif page == "📊 Evaluation":
    show_evaluation_page()

elif page == "📈 Analytics":
    show_analytics_page()

elif page == "📚 History":
    show_history_page()
# ==================================================
# FOOTER
# ==================================================

st.sidebar.markdown("---")
st.sidebar.caption("🚀 AI Interview Coach")

try:
    st.sidebar.caption(f"Version {APP_VERSION}")
except NameError:
    st.sidebar.caption("Version 1.0.0")
    
    