import streamlit as st


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
            st.success(
                "✅ Resume Uploaded"
            )
        else:
            st.info(
                "1️⃣ Resume Upload"
            )

    with col2:

        if questions_generated:
            st.success(
                "✅ Questions Generated"
            )
        else:
            st.info(
                "2️⃣ Generate Questions"
            )

    with col3:

        if interview_completed:
            st.success(
                "✅ Interview Completed"
            )
        else:
            st.info(
                "3️⃣ Interview"
            )

    with col4:

        if evaluation_generated:
            st.success(
                "✅ Evaluation Ready"
            )
        else:
            st.info(
                "4️⃣ Evaluation"
            )