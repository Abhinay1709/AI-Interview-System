import streamlit as st

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

# ==================================================
# PART 3: INTERVIEW PAGE       
# ==================================================
def show_interview_page():
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
