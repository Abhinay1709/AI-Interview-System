import streamlit as st


# ==========================================
# READINESS SCORE
# ==========================================

def calculate_readiness(
    ats_score,
    latest_score
):

    return round(

        (
            ats_score +
            (float(latest_score) * 10)
        ) / 2,

        2
    )


# ==========================================
# TOP DASHBOARD METRICS
# ==========================================

def show_dashboard_metrics(
    stats,
    latest_score,
    ats_score
):

    readiness = calculate_readiness(
        ats_score,
        latest_score
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Interviews",
            stats.get(
                "total_interviews",
                0
            )
        )

    with col2:
        st.metric(
            "Average Score",
            f"{stats.get('average_overall',0)}/10"
        )

    with col3:
        st.metric(
            "Best Score",
            f"{stats.get('best_score',0)}/10"
        )

    with col4:
        st.metric(
            "Readiness",
            f"{readiness}%"
        )


# ==========================================
# RESUME SUMMARY
# ==========================================

def show_resume_summary(
    skills,
    projects,
    latest_score
):

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Skills Found",
            len(skills)
        )

    with c2:
        st.metric(
            "Projects Found",
            len(projects)
        )

    with c3:
        st.metric(
            "Questions",
            10
        )

    with c4:
        st.metric(
            "Latest Score",
            latest_score
        )


# ==========================================
# CANDIDATE DETAILS
# ==========================================

def show_candidate_details(
    resume_details
):

    if not resume_details:

        st.info(
            "Upload a resume to view candidate details."
        )

        return

    st.subheader("👤 Candidate")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Name:** {resume_details.get('name','N/A')}"
        )

        st.write(
            f"**Email:** {resume_details.get('email','N/A')}"
        )

    with col2:

        st.write(
            f"**Phone:** {resume_details.get('phone','N/A')}"
        )


# ==========================================
# SYSTEM STATUS
# ==========================================

def show_system_status(
    resume_uploaded,
    questions_generated,
    interview_completed
):


    c1, c2, c3 = st.columns(3)

    with c1:

        if resume_uploaded:
            st.success(
                "Resume Uploaded"
            )
        else:
            st.warning(
                "Resume Not Uploaded"
            )

    with c2:

        if questions_generated:
            st.success(
                "Questions Generated"
            )
        else:
            st.warning(
                "Questions Not Generated"
            )

    with c3:

        if interview_completed:
            st.success(
                "Interview Completed"
            )
        else:
            st.warning(
                "Interview Not Completed"
            )
# ==========================================
# INTERVIEW STATUS TRACKER
# ==========================================

def show_interview_tracker(
    resume_uploaded,
    questions_generated,
    interview_completed,
    evaluation_generated
):

    st.subheader(
        "📍 Interview Progress"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        if resume_uploaded:
            st.success("✅ Resume")
        else:
            st.error("❌ Resume")

    with col2:

        if questions_generated:
            st.success("✅ Questions")
        else:
            st.error("❌ Questions")

    with col3:

        if interview_completed:
            st.success("✅ Interview")
        else:
            st.error("❌ Interview")

    with col4:

        if evaluation_generated:
            st.success("✅ Evaluation")
        else:
            st.error("❌ Evaluation")


def show_placement_summary(
    readiness,
    probability
):
    st.subheader(
        "🎯 Placement Summary"
    )
    c1, c2 = st.columns(2)
    with c1:
        st.metric(
            "Readiness",
            f"{readiness}%"
        )
    with c2:
        st.metric(
            "Placement Chance",
            f"{probability}%"
        )
    if probability >= 80:
        st.success(
            "Ready for placements"
        )
    elif probability >= 60:
        st.warning(
            "Almost ready"
        )
    else:
        st.error(
            "Needs preparation"
        )