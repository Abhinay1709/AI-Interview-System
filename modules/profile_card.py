import streamlit as st


# ==========================================
# PROFILE CARD
# ==========================================

def show_profile_card(
    resume_details,
    skills,
    projects,
    ats_score,
    readiness
):

    if not resume_details:
        return

    st.markdown(
        """
        <style>
        .profile-card{
            background:#1e293b;
            padding:25px;
            border-radius:18px;
            border:1px solid #334155;
            margin-bottom:20px;
        }

        .profile-title{
            font-size:24px;
            font-weight:700;
            color:white;
        }

        .profile-item{
            color:#cbd5e1;
            font-size:15px;
            margin-top:8px;
        }

        .profile-badge{
            background:#0ea5e9;
            padding:6px 12px;
            border-radius:12px;
            color:white;
            margin-right:6px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="profile-card">

        <div class="profile-title">
        👤 Candidate Profile
        </div>

        <div class="profile-item">
        <b>Name:</b> {resume_details.get('name','N/A')}
        </div>

        <div class="profile-item">
        <b>Email:</b> {resume_details.get('email','N/A')}
        </div>

        <div class="profile-item">
        <b>Phone:</b> {resume_details.get('phone','N/A')}
        </div>

        <br>

        <div class="profile-item">
        📚 Skills: {len(skills)}
        </div>

        <div class="profile-item">
        📂 Projects: {len(projects)}
        </div>

        <div class="profile-item">
        🎯 ATS Score: {ats_score}/100
        </div>

        <div class="profile-item">
        🚀 Readiness: {readiness}%
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )
    
def show_readiness_card(
    readiness
):

    st.markdown(
        f"""
        <div style="
            background:#1e293b;
            padding:20px;
            border-radius:20px;
            text-align:center;
            border:1px solid #334155;
        ">

        <h2 style="color:white">
        🎯 Placement Readiness
        </h2>

        <h1 style="
            color:#38bdf8;
            font-size:48px;
        ">
        {readiness}%
        </h1>

        </div>
        """,
        unsafe_allow_html=True
    )