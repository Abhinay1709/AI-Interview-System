import streamlit as st

from modules.answer_evaluator import (
    evaluate_full_interview
)

from modules.database_manager import (
    save_interview
)

from modules.score_parser import (
    extract_scores,
    get_question_score,
    get_model_answer,
    get_feedback
)

from modules.charts import (
    create_radar_chart
)

from modules.skill_gap_analyzer import (
    analyze_skill_gap
)

from modules.report_generator import (
    generate_full_report
)

from modules.candidate_intelligence import (
    calculate_placement_probability,
    get_best_career_path
)

from modules.answer_manager import (
    get_interview_statistics
)
# ==================================================
# PART 4: EVALUATION PAGE
# ==================================================
def show_evaluation_page():
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
                    progress = st.progress(0)
                    for i in range(100):
                        progress.progress(i + 1)

                    try:
                        evaluation = evaluate_full_interview(
                            st.session_state.questions,
                            st.session_state.question_answers
                        )
                    except Exception as e:
                        st.error(
                            f"Evaluation Failed: {str(e)}"
                        )
                        st.stop()
                    
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
                try:
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
                except Exception as e:
                    st.error(
                        f"Database Save Failed:{str(e)}"
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
            technical = float(
                scores.get("technical", 0)
            )
            communication = float(
                scores.get("communication", 0)
            )
            confidence = float(
                scores.get("confidence", 0)
            )
            fig = create_radar_chart(
                technical,
                communication,
                confidence
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

            st.divider()
            st.subheader(
                "🎯 Placement Probability"
            )
            placement_probability = (
                calculate_placement_probability(
                    ats_score,
                    interview_score
                )
            )
            st.metric(
                "Placement Probability",
                f"{placement_probability}%"
            )
            st.progress(
                placement_probability / 100
            )

            best_role = get_best_career_path(
                st.session_state.skills
            )
            st.success(
                f"Recommended Career Path: {best_role}"
            )

            st.divider()
            st.subheader(
                "🧠 AI Insights"
            )
            overall = float(
                scores.get(
                    "overall",
                    0
                )
            )
            if overall >= 8:
                st.success(
                    "Strong interview performance."
                )
            elif overall >= 6:
                st.warning(
                    "Average performance with room for improvement."
                )
            else:
                st.error(
                    "Interview performance needs improvement."
                )
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

            # DOWNLOAD REPORT (Updated Key here to be unique)
            report = generate_full_report(
                st.session_state.questions,
                st.session_state.question_answers,
                evaluation_text
            )

            st.download_button(
                "📄 Download Interview Report",
                report,
                file_name="Interview_Report.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
                key="download_current_interview_report" 
            )