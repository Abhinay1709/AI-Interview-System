import streamlit as st
import pandas as pd

from modules.database_manager import (
    get_all_interviews,
    normalize_interview_record
)

from modules.analytics import (
    calculate_statistics
)

from modules.dashboard import (
    calculate_readiness,
    show_dashboard_metrics,
    show_resume_summary,
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

def show_dashboard_page():
    # ==================================================
    # DASHBOARD PAGE
    # ==================================================
    st.header("🏠 Dashboard")
    if not st.session_state.resume_text:
        st.info(
            "Upload a resume to unlock dashboard insights."
        )
        st.stop()
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
    latest_score = (
        records[0][8]
        if records else 0
    )

    show_dashboard_metrics(
        stats,
        latest_score,
        st.session_state.get(
            "ats_score",
            0
        )
    )
    st.divider()

    # RESUME INFORMATION
    st.subheader("📄 Resume Summary")

    resume_details = st.session_state.get("resume_details", {})
    skills = st.session_state.get("skills", [])
    projects = st.session_state.get("projects", [])
    show_resume_summary(
        skills,
        projects,
        latest_score
    )

    readiness = calculate_readiness(
        st.session_state.get(
            "ats_score",
            0
        ),
        latest_score
    )

    show_profile_card(
        resume_details,
        skills,
        projects,
        st.session_state.get(
            "ats_score",
            0
        ),
        readiness
    )

    show_readiness_card(
        readiness
    )

    placement_probability = (
        calculate_placement_probability(
            st.session_state.get(
                "ats_score",
                0
            ),
            latest_score
        )
    )
    show_placement_summary(
        readiness,
        placement_probability
    )

    st.divider()
    show_interview_tracker(
        bool(
            st.session_state.resume_text
        ),
        bool(
            st.session_state.questions
        ),
        st.session_state.interview_finished,
        st.session_state.interview_completed
    )
    
    st.divider()
    st.subheader(
        "🎯 Recommended Roles"
    )
    role_matches = calculate_role_matches(
        skills
    )
    for role in role_matches[:3]:
        st.write(
            f"### {role['role']}"
        )
        st.progress(
            role["score"] / 100
        )
        st.caption(
            f"{role['score']}% Match"
        )

    st.divider()
    st.subheader(
        "🏅 Achievements"
    )
    if st.session_state.ats_score >= 80:
        st.success(
            "ATS Expert Badge"
        )
    if len(skills) >= 10:
        st.success(
            "Skill Master Badge"
        )
    if st.session_state.interview_completed:
        st.success(
            "Interview Completed Badge"
        )
    if records:
        latest_score = float(
            records[0][8]
        )
        if latest_score >= 8:
            st.success(
                "Top Performer Badge"
            )

    st.divider()
    st.subheader(
        "📊 Resume Match Score"
    )
    match_score = calculate_resume_match(
        skills,
        st.session_state.job_role
    )
    st.metric(
        "Match Score",
        f"{match_score}%"
    )
    st.progress(
        match_score / 100
    )

    st.divider()
    st.subheader(
        "📚 Career Recommendation"
    )
    if match_score >= 80:
        st.success(
            "Your profile is strongly aligned with this role."
        )
    elif match_score >= 60:
        st.warning(
            "You are close. Improve missing skills for better readiness."
        )
    else:
        st.error(
            "Significant skill gaps exist for this role."
        )

    st.divider()
    st.subheader(
        "🧠 Candidate Intelligence"
    )
    best_role = get_best_career_path(
        skills
    )
    st.success(
        f"Best Career Path: {best_role}"
    )

    roadmap = get_learning_roadmap(
        skills,
        best_role
    )

    st.markdown(
        "### 📚 Learning Roadmap"
    )

    for index, skill in enumerate(
        roadmap,
        start=1
    ):

        st.info(
            f"{index}. {skill}"
        )

    st.divider()
    st.subheader(
        "🚀 Quick Actions"
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button(
            "📄 Analyze Resume"
        ):
            st.session_state.current_page = (
                "📄 Resume Analysis"
            )
            st.rerun()
    with c2:
        if st.button(
            "🎯 Start Interview"
        ):
            st.session_state.current_page = (
                "🎯 Interview"
            )
            st.rerun()
    with c3:
        if st.button(
            "📈 View Analytics"
        ):
            st.session_state.current_page = (
                "📈 Analytics"
            )
            st.rerun()

    st.divider()
    # SYSTEM STATUS
    st.subheader("🚀 System Status")

    show_system_status(
        bool(
            st.session_state.resume_text
        ),
        bool(
            st.session_state.questions
        ),
        st.session_state.interview_completed
    )
