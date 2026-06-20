# ==================================================
# PART 1: MAIN APPLICATION
# ==================================================
# IMPORTS
# ==================================================

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
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

# ==================================================
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

st.sidebar.markdown("# 🚀 AI Interview Coach")
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
st.sidebar.markdown(
    """
### Workflow
✅ Resume Upload
✅ Skill Detection
✅ Question Generation
✅ Interview Practice
✅ Evaluation
✅ Analytics
✅ Report Download
"""
)

# ==================================================
# DASHBOARD PAGE
# ==================================================

if page == "🏠 Dashboard":

    st.header("🏠 Dashboard")

    records = get_all_interviews()
    stats = calculate_statistics(records)

    # ==========================================
    # SCORE TREND DATA
    # ==========================================

    trend_data = []

    for index, record in enumerate(reversed(records), start=1):
        normalized = normalize_interview_record(record)
        trend_data.append({
            "Interview": index,
            "Technical": float(normalized.get("technical_score", 0)),
            "Communication": float(normalized.get("communication_score", 0)),
            "Confidence": float(normalized.get("confidence_score", 0)),
            "Overall": float(normalized.get("overall_score", 0))
        })
    
    # DATAFRAME
    if trend_data:
        trend_df = pd.DataFrame(trend_data)        

    # TOP METRICS
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Interviews", stats.get("total_interviews", 0))

    with col2:
        st.metric("Average Score", f"{stats.get('average_overall', 0)}/10")

    with col3:
        st.metric("Best Score", f"{stats.get('best_score', 0)}/10")

    with col4:
        latest_score = (
            records[0][8]
            if records else 0
        )
        readiness = round(
            (
                st.session_state.get(
                    "ats_score",
                    0
                )
                +
                (
                    float(
                        latest_score
                    ) * 10
                )
            ) / 2,
            2
        )
        st.metric(
            "Readiness",
            f"{readiness}%"
        )
        

    st.divider()

    # RESUME INFORMATION
    st.subheader("📄 Resume Summary")

    resume_details = st.session_state.get("resume_details", {})
    skills = st.session_state.get("skills", [])
    projects = st.session_state.get("projects", [])

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Skills Found", len(skills))

    with c2:
        st.metric("Projects Found", len(projects))

    with c3:
        st.metric("Questions", 10)

    with c4:
        latest_score = (records[0][8] if records else 0)
        st.metric("Latest Score", latest_score)

    st.divider()

    # CANDIDATE DETAILS
    if resume_details:
        st.subheader("👤 Candidate")
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Name:** {resume_details.get('name', 'N/A')}")
            st.write(f"**Email:** {resume_details.get('email', 'N/A')}")

        with col2:
            st.write(f"**Phone:** {resume_details.get('phone', 'N/A')}")
    else:
        st.info("Upload a resume to view candidate details.")

    st.divider()

    # SYSTEM STATUS
    st.subheader("🚀 System Status")

    status_col1, status_col2, status_col3 = st.columns(3)

    with status_col1:
        if st.session_state.resume_text:
            st.success("Resume Uploaded")
        else:
            st.warning("Resume Not Uploaded")

    with status_col2:
        if st.session_state.questions:
            st.success("Questions Generated")
        else:
            st.warning("Questions Not Generated")

    with status_col3:
        if st.session_state.interview_completed:
            st.success("Interview Completed")
        else:
            st.warning("Interview Not Completed")

# ==================================================
# PART 2: RESUME ANALYSIS
# ==================================================

if page == "📄 Resume Analysis":

    st.header("📄 Resume Upload")

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx", "txt"]
    )

    # PROCESS RESUME
    if uploaded_file is not None:
        resume_text = extract_resume_text(uploaded_file)

        if validate_resume(resume_text):
            # SAVE SESSION DATA
            st.session_state.resume_text = resume_text
            resume_details = extract_resume_details(resume_text)
            
            st.session_state.resume_details = resume_details
            st.session_state.skills = resume_details.get("skills", [])
            st.session_state.projects = resume_details.get("projects", [])

            st.success("✅ Resume Parsed Successfully")

            # ats score 
            ats = calculate_ats_score(resume_text)
            
            st.session_state.ats_score = (
                ats["score"]
            )
            st.divider()
            st.subheader("🎯 ATS Resume Score")

            st.metric("ATS Score", f"{ats['score']}/100")

            col1, col2 = st.columns(2)

            with col1:
                st.success("\n".join([f"✓ {item}" for item in ats["strengths"]]))

            with col2:
                st.warning("\n".join([f"✗ {item}" for item in ats["missing"]]))

            st.info("\n".join([f"• {item}" for item in ats["suggestions"]]))

            # resume insights
            insights = generate_resume_insights(resume_details, ats)

            st.divider()
            st.subheader("📈 Resume Insights")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 💪 Strengths")
                for item in insights["strengths"]:
                    st.success(item)

            with col2:
                st.markdown("### ⚠ Areas To Improve")
                for item in insights["improvements"]:
                    st.warning(item)

            st.markdown("### 📚 Recommendations")
            for item in insights["recommendations"]:
                st.info(item)

            # DASHBOARD
            st.markdown("## 📊 Candidate Dashboard")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Skills", len(st.session_state.skills))
            with col2:
                st.metric("Projects", len(st.session_state.projects))
            with col3:
                st.metric("Resume Pages", max(1, len(resume_text.split("\n")) // 40))
            with col4:
                st.metric("Questions", 10)

            # CANDIDATE DETAILS
            st.divider()
            st.subheader("👤 Candidate Details")

            c1, c2 = st.columns(2)

            with c1:
                st.write(f"**Name:** {resume_details.get('name', 'N/A')}")
                st.write(f"**Email:** {resume_details.get('email', 'N/A')}")

            with c2:
                st.write(f"**Phone:** {resume_details.get('phone', 'N/A')}")

            # RESUME PREVIEW
            st.divider()

            with st.expander("📄 View Resume Content"):
                st.text_area("Resume", resume_text, height=350)

            # SKILLS
            st.divider()
            st.subheader("🛠 Detected Skills")

            skills_html = '<div style="display:flex; flex-wrap:wrap; gap:10px; margin-top:10px;">'
            for skill in st.session_state.skills:
                skills_html += f'<span style="background:#0ea5e9; color:white; padding:8px 16px; border-radius:20px; font-weight:600; display:inline-block;">{skill}</span>'
            skills_html += "</div>"

            st.markdown(skills_html, unsafe_allow_html=True)

            # SKILL CATEGORIES
            categorized_skills = extract_skills_by_category(resume_text)
            st.divider()
            
            if categorized_skills:
                st.markdown("### 📚 Skills by Category")
                for category, skill_list in categorized_skills.items():
                    with st.expander(category):
                        st.write(", ".join(skill_list))

            # PROJECTS
            st.divider()
            st.subheader("📂 Detected Projects")

            filtered_projects = []
            for project in st.session_state.projects:
                project = project.strip()
                if len(project.split()) <= 6 and not project.startswith("•"):
                    filtered_projects.append(project)

            filtered_projects = list(set(filtered_projects))

            if filtered_projects:
                for project in filtered_projects:
                    st.success(project)
            else:
                st.info("No project titles detected.")

        else:
            st.error("❌ Invalid Resume Uploaded")

    else:
        st.info("Upload a resume to begin analysis.")
        
# ==================================================
# PART 3: INTERVIEW PAGE       
# ==================================================

if page == "🎯 Interview":
    st.header("🎯 AI Interview")
    
    # RESUME CHECK
    if not st.session_state.resume_text:
        st.warning("⚠ Please upload and analyze your resume first.")
    else:
        # GENERATE QUESTIONS
        if not st.session_state.questions:
            
            st.subheader("⚙ Interview Settings")

            difficulty_options = [
                "Beginner",
                "Intermediate",
                "Advanced"
            ]

            difficulty = st.selectbox(
                "Select Difficulty",
                difficulty_options,
                index=difficulty_options.index(
                    st.session_state.difficulty
                ),
                key="difficulty_selector"
            )

            st.session_state.difficulty = difficulty

            st.selectbox(
                "Select Job Role",
                [
                    "AI Engineer",
                    "ML Engineer",
                    "Data Analyst",
                    "Python Developer",
                    "Software Engineer",
                    "Full Stack Developer"
                ],
                key="job_role"
            )
            st.info(
                f"Role: {st.session_state.job_role} | "
                f"Difficulty: {st.session_state.difficulty}"
            )

            st.info("Generate interview questions based on your resume.")

            if st.button("🚀 Generate Questions", type="primary"):
                with st.spinner("Generating Questions..."):
                    question_list = generate_questions(
                        st.session_state.resume_text,
                        st.session_state.skills,
                        st.session_state.projects,
                        st.session_state.difficulty,
                        st.session_state.job_role
                    )

                st.session_state.questions = question_list
                st.session_state.current_question_index = 0
                st.session_state.question_answers = {}
                st.session_state.final_evaluation = ""
                st.session_state.interview_finished = False
                st.session_state.interview_completed = False
                st.session_state.auto_saved = False

                st.success("✅ 10 Questions Generated Successfully")
                st.rerun()

        # QUESTIONS GENERATED
        if st.session_state.questions:
            total_questions = len(st.session_state.questions)
            current_index = st.session_state.current_question_index
            current_question = st.session_state.questions[current_index]

            # PROGRESS BAR
            progress = (current_index + 1) / total_questions
            st.progress(progress)
            st.markdown(f"### Question {current_index + 1} of {total_questions}")

            # SIDEBAR STATS
            answered_count = get_answered_count(st.session_state.question_answers)
            skipped_count = get_skipped_count(st.session_state.questions, st.session_state.question_answers)

            st.sidebar.metric("Answered", answered_count)
            st.sidebar.metric("Skipped", skipped_count)

            # QUESTION CARD
            st.info(current_question)
            st.caption(
                "If you don't know the answer, enter: ( No, N/A, Skip )\n"
                "These will be treated as skipped answers."
            )

            # EXISTING ANSWER
            existing_answer = st.session_state.question_answers.get(current_question, "")

            answer_text = st.text_area(
                "✍ Your Answer",
                value=existing_answer,
                height=200,
                key=f"answer_{current_index}"
            )

            # VOICE INPUT
            voice_col1, voice_col2 = st.columns([1, 4])

            with voice_col1:
                if st.button("🎙 Record"):
                    with st.spinner("Listening..."):
                        voice_text = listen_and_convert()
                        voice_text = clean_speech_text(voice_text)

                        if voice_text:
                            st.session_state.question_answers[current_question] = voice_text
                            st.success("Voice Answer Recorded")
                            st.rerun()

            # NAVIGATION
            st.divider()

            nav1, nav2 = st.columns(2)
            is_last_question = (current_index == total_questions - 1)

            with nav1:
                if st.button("⬅ Previous"):
                    st.session_state.question_answers[current_question] = answer_text
                    if current_index > 0:
                        st.session_state.current_question_index -= 1
                        st.rerun()

            with nav2:
                if not is_last_question:
                    if st.button("➡ Save & Next", type="primary"):
                        st.session_state.question_answers[current_question] = answer_text
                        st.session_state.current_question_index += 1
                        st.rerun()
                else:
                    if st.button("🎯 Finish Interview", type="primary"):
                        st.session_state.question_answers[current_question] = answer_text
                        st.session_state.interview_finished = True
                        st.success(
                            "✅ Interview Completed Successfully!"
                        )
                        st.info(
                            "📊 Your interview is ready for evaluation."
                        )
                        st.balloons()
                        st.session_state.show_evaluation_button = True
                        st.rerun()

            # LIVE INTERVIEW STATS
            if st.session_state.show_evaluation_button:
                st.divider()
                st.success(
                    "✅ Interview Completed Successfully"
                )
                st.info(
                    "📊 Ready to generate your evaluation report."
                )
                if st.button(
                    "🚀 Go To Evaluation",
                    type="primary"
                ):
                    st.session_state.current_page = "📊 Evaluation"
                    st.session_state.show_evaluation_button = False
                    st.rerun()

            st.divider()
            stats = get_interview_statistics(
                st.session_state.questions,
                st.session_state.question_answers
            )
            s1, s2, s3 = st.columns(3)
            with s1:
                st.metric("Answered", stats["answered_questions"])
            with s2:
                st.metric("Skipped", stats["skipped_questions"])
            with s3:
                st.metric("Completion %", f"{stats['completion_percentage']}%")
                
# ==================================================
# PART 4: EVALUATION PAGE
# ==================================================

if page == "📊 Evaluation":

    st.header("📊 Interview Evaluation")

    # INTERVIEW NOT COMPLETED
    if not st.session_state.interview_finished:
        st.info(
            "Complete the interview first.\n"
            "Go to the Interview page and answer all questions before generating evaluation."
        )

    else:
        # GENERATE EVALUATION
        if not st.session_state.interview_completed:
            stats = get_interview_statistics(
                st.session_state.questions,
                st.session_state.question_answers
            )

            st.subheader("Interview Summary")

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric("Questions", stats["total_questions"])
            with c2:
                st.metric("Answered", stats["answered_questions"])
            with c3:
                st.metric("Skipped", stats["skipped_questions"])
            with c4:
                st.metric("Completion %", f"{stats['completion_percentage']}%")

            st.divider()

            if st.button("🚀 Generate Evaluation", type="primary"):
                with st.spinner("Evaluating Interview..."):
                    evaluation = evaluate_full_interview(
                        st.session_state.questions,
                        st.session_state.question_answers
                    )
                    
                    st.text_area("Raw Evaluation Output", evaluation, height=400)

                st.session_state.final_evaluation = evaluation
                st.session_state.interview_completed = True
                st.rerun()

        # SHOW EVALUATION
        if st.session_state.interview_completed:
            evaluation_text = st.session_state.final_evaluation
            scores = extract_scores(evaluation_text)

            # AUTO SAVE
            if not st.session_state.auto_saved:
                save_interview(
                    questions=st.session_state.questions,
                    answers=st.session_state.question_answers,
                    evaluation=evaluation_text,
                    technical_score=scores["technical"],
                    communication_score=scores["communication"],
                    confidence_score=scores["confidence"],
                    overall_score=scores["overall"],
                    total_questions=scores["total_questions"],
                    answered_questions=scores["attempted"],
                    skipped_questions=scores["skipped"],
                    completion_percentage=scores["completion_percentage"],
                    strengths=scores["strengths"],
                    weaknesses=scores["weaknesses"],
                    suggestions=scores["suggestions"]
                )

                st.session_state.auto_saved = True
                st.success("Interview Saved Successfully")

            # SCORE CARDS
            st.subheader("🏆 Overall Scores")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Technical", f"{scores.get('technical', '0')}/10")
            with col2:
                st.metric("Communication", f"{scores.get('communication', '0')}/10")
            with col3:
                st.metric("Confidence", f"{scores.get('confidence', '0')}/10")
            with col4:
                st.metric("Overall", f"{scores.get('overall', '0')}/10")

            # INTERVIEW STATS
            st.divider()

            s1, s2, s3, s4 = st.columns(4)

            with s1:
                st.metric("Total Questions", scores.get("total_questions", 0))
            with s2:
                st.metric("Answered", scores.get("attempted", 0))
            with s3:
                st.metric("Skipped", scores.get("skipped", 0))
            with s4:
                st.metric("Completion %", f"{scores.get('completion_percentage', 0)}%")

            # QUESTION ANALYSIS
            st.divider()
            st.subheader("📝 Question-wise Analysis")

            question_options = [
                f"Question {i}"
                for i in range(1, len(st.session_state.questions) + 1)
            ]

            selected_question = st.radio(
                "Select Question",
                question_options,
                horizontal=True
            )

            selected_index = int(selected_question.split()[-1])
            question = st.session_state.questions[selected_index - 1]
            answer = st.session_state.question_answers.get(question, "No Answer")
            question_score = get_question_score(evaluation_text, selected_index)
            model_answer = get_model_answer(evaluation_text, selected_index)
            feedback = get_feedback(evaluation_text, selected_index)

            st.markdown(f"## {selected_question}")
            st.markdown("### Question")
            st.write(question)
            st.markdown("### My Answer")
            st.write(answer)

            col1, col2 = st.columns([1, 4])

            with col1:
                st.metric("Score", f"{question_score}/10")

            st.markdown("### Model Answer")
            st.info(model_answer)
            st.markdown("### Feedback")
            st.warning(feedback)

            # PERFORMANCE RADAR CHART
            st.divider()
            st.subheader("🎯 Performance Radar")
            
            technical = float(scores.get("technical", 0))
            communication = float(scores.get("communication", 0))
            confidence = float(scores.get("confidence", 0))
            
            # Derived values
            project_knowledge = round((technical + confidence) / 2, 1)
            problem_solving = round((technical + communication) / 2, 1)
            
            categories = [
                "Technical",
                "Communication",
                "Confidence",
                "Project Knowledge",
                "Problem Solving"
            ]

            values = [
                technical,
                communication,
                confidence,
                project_knowledge,
                problem_solving
            ]

            values.append(values[0])
            categories.append(categories[0])

            fig = go.Figure()

            fig.add_trace(
                go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill="toself",
                    name="Performance"
                )
            )

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 10]
                    )
                ),
                showlegend=False,
                height=500
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )
            
            # READINESS SCORE
            st.divider()
            st.subheader("🎯 Interview Readiness Score")
            
            ats_score = float(st.session_state.get("ats_score", 0))
            interview_score = float(scores.get("overall", 0))
            
            readiness_score = round(
                (ats_score + (interview_score * 10)) / 2,
                2
            )
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("ATS Score", f"{ats_score}/100")
            with col2:
                st.metric("Interview Score", f"{interview_score}/10")
            with col3:
                st.metric("Readiness", f"{readiness_score}%")
                
            if readiness_score >= 85:
                st.success("🟢 Placement Ready")
            elif readiness_score >= 70:
                st.warning("🟡 Almost Ready")
            else:
                st.error("🔴 Needs More Preparation")
                
            st.progress(min(readiness_score / 100, 1.0))
            st.caption(f"Readiness Level: {readiness_score}%")

            # SKILL GAP ANALYSIS
            st.divider()
            st.subheader("🎯 Skill Gap Analysis")
            
            gap_result = analyze_skill_gap(
                st.session_state.skills,
                st.session_state.job_role
            )

            st.info(f"Target Role: {st.session_state.job_role}")
            left, right = st.columns(2)
            
            with left:
                st.markdown("### ✅ Current Skills")
                if gap_result["current_skills"]:
                    for skill in gap_result["current_skills"]:
                        st.success(skill)
                else:
                    st.warning("No matching skills found.")
                    
            with right:
                st.markdown("### ❌ Missing Skills")
                if gap_result["missing_skills"]:
                    for skill in gap_result["missing_skills"]:
                        st.error(skill)
                else:
                    st.success("No skill gaps detected.")
                    
            st.divider()
            st.metric("Role Readiness", f"{gap_result['readiness']}%")
            st.progress(gap_result["readiness"] / 100)
            
            st.markdown("### 📚 Next Learning Priorities")
            for index, skill in enumerate(gap_result["missing_skills"][:5], start=1):
                st.info(f"{index}. {skill}")

            # STRENGTHS
            st.divider()
            st.subheader("💪 Strengths")
            st.success(scores.get("strengths", ""))
            
            # WEAKNESSES
            st.subheader("⚠ Weaknesses")
            st.warning(scores.get("weaknesses", ""))
            
            # SUGGESTIONS
            st.subheader("📚 Suggestions")
            st.info(scores.get("suggestions", ""))
            
            # FULL EVALUATION
            with st.expander("📄 View Full Evaluation", expanded=False):
                for index, question in enumerate(st.session_state.questions, start=1):
                    answer = st.session_state.question_answers.get(question, "No Answer")
                    question_score = get_question_score(evaluation_text, index)
                    model_answer = get_model_answer(evaluation_text, index)
                    feedback = get_feedback(evaluation_text, index)

                    st.markdown(f"## Question {index}")
                    st.markdown(f"**Question:**\n\n{question}")
                    st.markdown(f"**My Answer:**\n\n{answer}")
                    st.markdown(f"**Score:** {question_score}/10")
                    st.markdown("**Model Answer:**")
                    st.info(model_answer)
                    st.markdown("**Feedback:**")
                    st.warning(feedback)
                    st.divider()

                st.subheader("🏆 Overall Scores")
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Technical", scores.get("technical", "0"))
                with col2:
                    st.metric("Communication", scores.get("communication", "0"))
                with col3:
                    st.metric("Confidence", scores.get("confidence", "0"))
                with col4:
                    st.metric("Overall", scores.get("overall", "0"))

                st.divider()
                st.subheader("💪 Strengths")
                st.success(scores.get("strengths", ""))
                st.subheader("⚠ Weaknesses")
                st.warning(scores.get("weaknesses", ""))
                st.subheader("📚 Suggestions")
                st.info(scores.get("suggestions", ""))

            # DOWNLOAD REPORT
            report = generate_full_report(
                st.session_state.questions,
                st.session_state.question_answers,
                evaluation_text
            )

            st.download_button(
                "📥 Download Report",
                report,
                file_name="Interview_Report.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            
# ==================================================
# PART 5: ANALYTICS DETAILS
# ==================================================

if page == "📈 Analytics":

    st.header("📈 Analytics Dashboard")

    records = get_all_interviews()
    stats = calculate_statistics(records)

    latest_record = None
    if records:
        latest_record = normalize_interview_record(
            records[0]
        )

    normalized_records = [
        normalize_interview_record(record)
        for record in records
    ]

    # Re-calculate trend data globally for this render
    trend_data = []
    for index, record in enumerate(reversed(records), start=1):
        normalized = normalize_interview_record(record)
        trend_data.append({
            "Interview": index,
            "Technical": float(normalized.get("technical_score", 0)),
            "Communication": float(normalized.get("communication_score", 0)),
            "Confidence": float(normalized.get("confidence_score", 0)),
            "Overall": float(normalized.get("overall_score", 0))
        })

    # SCORE CARDS
    row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)

    with row1_col1:
        st.metric("Total Interviews", stats.get("total_interviews", 0))
    with row1_col2:
        st.metric("Avg Technical", f"{stats.get('average_technical', 0)}/10")
    with row1_col3:
        st.metric("Avg Communication", f"{stats.get('average_communication', 0)}/10")
    with row1_col4:
        st.metric("Avg Confidence", f"{stats.get('average_confidence', 0)}/10")

    row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)

    with row2_col1:
        st.metric("Avg Overall", f"{stats.get('average_overall', 0)}/10")
    with row2_col2:
        st.metric("Best Score", f"{stats.get('best_score', 0)}/10")
    with row2_col3:
        st.metric("Worst Score", f"{stats.get('worst_score', 0)}/10")
    with row2_col4:
        st.metric("Completion Rate", f"{stats.get('completion_rate', 0)}%")

    if latest_record:
        
        st.divider()

        st.subheader("🎯 Latest Interview Radar")

        technical = float(latest_record.get("technical_score", 0))
        communication = float(latest_record.get("communication_score", 0))
        confidence = float(latest_record.get("confidence_score", 0))

        project_knowledge = round((technical + confidence) / 2, 1)
        problem_solving = round((technical + communication) / 2, 1)

        categories = [
            "Technical",
            "Communication",
            "Confidence",
            "Project Knowledge",
            "Problem Solving"
        ]

        values = [
            technical,
            communication,
            confidence,
            project_knowledge,
            problem_solving
        ]

        values.append(values[0])
        categories.append(categories[0])

        fig = go.Figure()

        fig.add_trace(
            go.Scatterpolar(
                r=values,
                theta=categories,
                fill="toself"
            )
        )

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
    
    # SCORE TREND CHART
    if trend_data:
        trend_df = pd.DataFrame(trend_data)
        
        # performance highlights
        st.divider()
        st.subheader("📌 Performance Highlights")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Latest Score",
                round(trend_df["Overall"].iloc[-1], 2)
            )

        with c2:
            st.metric(
                "Highest Score",
                round(trend_df["Overall"].max(), 2)
            )

        with c3:
            st.metric(
                "Lowest Score",
                round(trend_df["Overall"].min(), 2)
            )
            
        # performance trend
        st.divider()
        st.subheader("📈 Performance Trend")

        fig = px.line(
            trend_df,
            x="Interview",
            y="Overall",
            markers=True,
            title="Overall Score Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Multi line chart
        st.subheader("📊 Skill Score Trends")

        multi_fig = px.line(
            trend_df,
            x="Interview",
            y=[
                "Technical",
                "Communication",
                "Confidence"
            ],
            markers=True
        )

        st.plotly_chart(
            multi_fig,
            use_container_width=True
        )

    # INTERVIEW STATS
    st.divider()
    st.subheader("Interview Statistics")

    stat1, stat2 = st.columns(2)

    with stat1:
        st.metric("Attempted Questions", stats.get("attempted_questions", 0))
    with stat2:
        st.metric("Skipped Questions", stats.get("skipped_questions", 0))
    
    st.divider()
    st.subheader("📊 Interview Comparison")
    
    if len(records) >= 2:
        
        comparison_options = []

        for index, record in enumerate(records, start=1):
            normalized = normalize_interview_record(record)
            comparison_options.append(f"Interview {index} | {normalized.get('date', 'N/A')}")

        col1, col2 = st.columns(2)

        with col1:
            interview_1 = st.selectbox(
                "Select Interview 1",
                comparison_options,
                index=0
            )

        with col2:
            interview_2 = st.selectbox(
                "Select Interview 2",
                comparison_options,
                index=min(1, len(comparison_options) - 1)
            )

        idx1 = comparison_options.index(interview_1)
        idx2 = comparison_options.index(interview_2)

        record1 = normalize_interview_record(records[idx1])
        record2 = normalize_interview_record(records[idx2])
        
        st.divider()

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Technical",
                record2.get("technical_score", 0),
                delta=float(record2.get("technical_score", 0)) - float(record1.get("technical_score", 0))
            )

        with c2:
            st.metric(
                "Communication",
                record2.get("communication_score", 0),
                delta=float(record2.get("communication_score", 0)) - float(record1.get("communication_score", 0))
            )

        with c3:
            st.metric(
                "Confidence",
                record2.get("confidence_score", 0),
                delta=float(record2.get("confidence_score", 0)) - float(record1.get("confidence_score", 0))
            )

        with c4:
            st.metric(
                "Overall",
                record2.get("overall_score", 0),
                delta=float(record2.get("overall_score", 0)) - float(record1.get("overall_score", 0))
            )

        st.divider()

        left, right = st.columns(2)

        with left:
            st.markdown("### 💪 Interview 1 Strengths")
            st.success(record1.get("strengths", ""))

        with right:
            st.markdown("### 💪 Interview 2 Strengths")
            st.success(record2.get("strengths", ""))
            
# ==================================================
# HISTORY PAGE
# ==================================================

if page == "📚 History":

    st.header("📚 Interview History")

    records = get_all_interviews()

    if not records:
        st.info("No interview history available.")

    else:
        for interview_number, record in enumerate(records, start=1):
            normalized = normalize_interview_record(record)
            interview_id = normalized.get("id", str(interview_number))

            with st.expander(
                f"Interview {interview_number} | {normalized.get('date', 'Unknown Date')} | Score: {normalized.get('overall_score', 0)}/10"
            ):
                # SCORE CARDS
                c1, c2, c3, c4 = st.columns(4)

                with c1:
                    st.metric("Technical", normalized.get("technical_score", "0"))
                with c2:
                    st.metric("Communication", normalized.get("communication_score", "0"))
                with c3:
                    st.metric("Confidence", normalized.get("confidence_score", "0"))
                with c4:
                    st.metric("Overall", normalized.get("overall_score", "0"))

                # STRENGTHS
                st.subheader("💪 Strengths")
                st.success(normalized.get("strengths", ""))

                # WEAKNESSES
                st.subheader("⚠ Weaknesses")
                st.warning(normalized.get("weaknesses", ""))

                # SUGGESTIONS
                st.subheader("📚 Suggestions")
                st.info(normalized.get("suggestions", ""))

                # FULL EVALUATION
                with st.expander("View Full Evaluation"):
                    st.text_area(
                        "Evaluation",
                        str(normalized.get("evaluation", "")),
                        height=300,
                        key=f"eval_{interview_id}"
                    )

                # DOWNLOAD REPORT
                report = generate_full_report(
                    normalized.get("questions", []),
                    normalized.get("answers", {}),
                    normalized.get("evaluation", "")
                )

                st.download_button(
                    "📥 Download Report",
                    report,
                    file_name=f"Interview_{interview_id}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key=f"download_{interview_id}"
                )

                # DELETE INTERVIEW
                if st.button("🗑 Delete Interview", key=f"delete_{interview_id}"):
                    delete_interview(interview_id)
                    st.success("Interview Deleted")
                    st.rerun()

    # EXPORT HISTORY
    st.divider()
    st.header("📤 Export Interview History")

    if records:
        col1, col2 = st.columns(2)

        with col1:
            if st.button("📊 Generate Excel Export"):
                excel_file = export_history_to_excel(records)
                st.session_state["excel_file"] = excel_file
                st.success("Excel Generated")

        with col2:
            if "excel_file" in st.session_state:
                try:
                    with open(st.session_state["excel_file"], "rb") as file:
                        st.download_button(
                            "📥 Download Excel",
                            file,
                            file_name="Interview_History.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                except Exception:
                    st.warning("Generate Excel First")

    # HISTORY MANAGEMENT
    st.divider()
    st.header("⚠ History Management")

    if records:
        st.warning("This action permanently deletes all interview history.")

        if st.button("🗑 Delete Entire History"):
            clear_database()
            st.session_state.questions = []
            st.session_state.question_answers = {}
            st.session_state.final_evaluation = ""
            st.session_state.interview_finished = False
            st.session_state.interview_completed = False
            st.session_state.auto_saved = False
            
            st.success("History Deleted")
            st.rerun()

# ==================================================
# FOOTER
# ==================================================

st.sidebar.markdown("---")
st.sidebar.caption("🚀 AI Interview Coach")

try:
    st.sidebar.caption(f"Version {APP_VERSION}")
except NameError:
    st.sidebar.caption("Version 1.0.0")