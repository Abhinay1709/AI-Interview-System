import streamlit as st

from modules.resume_parser import (
    extract_resume_text,
    extract_resume_details,
    validate_resume
)

from modules.ats_analyzer import (
    calculate_ats_score
)

from modules.resume_insights import (
    generate_resume_insights
)

from modules.skill_extractor import (
    extract_skills_by_category
)

# ==================================================
# PART 2: RESUME ANALYSIS
# ==================================================
def show_resume_page():

    st.header("📄 Resume Upload")

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx", "txt"]
    )

    if uploaded_file is not None:
        
        if (
            st.session_state.last_resume
            != uploaded_file.name
        ):

            st.session_state.last_resume = uploaded_file.name

            st.session_state.resume_details = {}
            st.session_state.skills = []
            st.session_state.projects = []

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
        
