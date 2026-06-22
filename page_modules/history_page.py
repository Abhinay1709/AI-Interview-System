import streamlit as st
import pandas as pd
import plotly.express as px

from modules.database_manager import (
    get_all_interviews,
    delete_interview,
    clear_database,
    normalize_interview_record
)

from modules.report_generator import (
    generate_full_report
)

from modules.export_history import (
    export_history_to_excel
)


def show_history_page():
    st.header("📚 Interview History")
    records = get_all_interviews()

    if records:
        timeline = []
        for index, record in enumerate(
            reversed(records),
            start=1
        ):
            timeline.append({
                "Interview": index,
                "Score":
                float(record[8] or 0)
            })
        df = pd.DataFrame(
            timeline
        )
        fig = px.line(
            df,
            x="Interview",
            y="Score",
            markers=True,
            title="Interview Growth Timeline"
        )
        st.plotly_chart(
            fig,
            use_container_width=True
        )

    if records:
        best_score = max(
            [
                float(record[8] or 0)
                for record in records
            ]
        )
        average_score = round(
            sum(
                float(record[8] or 0)
                for record in records
            )
            /
            len(records),
            2
        )
        c1, c2 = st.columns(2)
        with c1:
            st.metric(
                "Best Score",
                best_score
            )
        with c2:
            st.metric(
                "Average Score",
                average_score
            )

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

                # RECONSTRUCT SCORES FOR PDF
                historical_scores = {
                    "overall": normalized.get("overall_score", "0"),
                    "technical": normalized.get("technical_score", "0"),
                    "communication": normalized.get("communication_score", "0"),
                    "confidence": normalized.get("confidence_score", "0")
                }

                # Updated Key here to be dynamic and unique per loop iteration
                st.download_button(
                    "📄 Download Interview Report",
                    report,
                    file_name=f"Interview_Report_{interview_id}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                    key=f"download_history_report_{interview_id}" 
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
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key="download_excel_history"
                        )
                except Exception:
                    st.warning("Generate Excel First")

    # HISTORY MANAGEMENT
    st.divider()
    st.header("⚠ History Management")

    if records:
        st.warning("This action permanently deletes all interview history.")

        if st.button(
            "💾 Backup Database"
        ):
            backup = backup_database()
            st.success(
                f"Backup Created: {backup}"
            )

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
