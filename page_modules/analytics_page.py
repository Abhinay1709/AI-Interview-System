import streamlit as st
import pandas as pd

from modules.database_manager import (
    get_all_interviews,
    normalize_interview_record
)

from modules.analytics import (
    calculate_statistics
)

from modules.charts import (
    create_radar_chart,
    create_score_trend_chart,
    create_skill_trend_chart
)

from modules.advanced_analytics import (
    calculate_improvement,
    calculate_consistency,
    strongest_area as get_strongest_area,
    weakest_area as get_weakest_area
)

# ==================================================
# PART 5: ANALYTICS DETAILS
# ==================================================
def show_analytics_page():
    st.header("📈 Analytics Dashboard")

    records = get_all_interviews()
    stats = calculate_statistics(records)

    latest_record = None
    best_record = None
    if records:
        best_record = max(
            records,
            key=lambda x: float(
                x[8] or 0
            )
        )
        best_record = normalize_interview_record(
            best_record
        )

    improvement = calculate_improvement(
        records
    )
    consistency = calculate_consistency(
        records
    )
    strong_area = get_strongest_area(stats)
    weak_area = get_weakest_area(stats)

    st.divider()
    st.subheader(
        "🧠 Advanced Insights"
    )
    c1, c2 = st.columns(2)
    with c1:
        if improvement > 0:
            st.metric(
                "Performance Change",
                f"+{improvement}"
            )
        elif improvement < 0:
            st.metric(
                "Performance Change",
                f"{improvement}"
            )
            st.warning(
                "Recent score is lower than earlier interviews."
            )
        else:
            st.metric(
                "Performance Change",
                "0"
            )
        st.metric(
            "Consistency",
            f"{consistency}%"
        )
    with c2:
        if strong_area == "Not Enough Data":
            st.info(
                "📭 Not enough interview data to identify strongest area."
            )
        else:
            st.success(
                f"Strongest Area: {strong_area}"
            )
        if weak_area == "Not Enough Data":
            st.info(
                "📭 Not enough interview data to identify weakest area."
            )
        else:
            st.warning(
                f"Weakest Area: {weak_area}"
            )

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
    st.divider()
    st.subheader(
        "🏆 Best Interview"
    )
    if not records:
        st.info("📭 No interviews available in history.")
    elif best_record:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(
                "Best Score",
                f"{best_record['overall_score']}/10"
            )
        with c2:
            st.metric(
                "Answered",
                best_record[
                    "answered_questions"
                ]
            )
        with c3:
            st.metric(
                "Completion %",
                best_record[
                    "completion_percentage"
                ]
            )
        st.success(
            best_record[
                "strengths"
            ]
        )

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
        technical = float(
            latest_record.get(
                "technical_score",
                0
            )
        )
        communication = float(
            latest_record.get(
                "communication_score",
                0
            )
        )
        confidence = float(
            latest_record.get(
                "confidence_score",
                0
            )
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

    # SCORE TREND CHART
    if trend_data:
        trend_df = pd.DataFrame(trend_data)

        st.divider()
        st.subheader(
            "🧠 Insights"
        )
        avg_tech = stats.get(
            "average_technical",
            0
        )
        avg_comm = stats.get(
            "average_communication",
            0
        )
        avg_conf = stats.get(
            "average_confidence",
            0
        )
        best_area = max(
            {
                "Technical": avg_tech,
                "Communication": avg_comm,
                "Confidence": avg_conf
            },
            key=lambda x: {
                "Technical": avg_tech,
                "Communication": avg_comm,
                "Confidence": avg_conf
            }[x]
        )
        weakest_area = min(
            {
                "Technical": avg_tech,
                "Communication": avg_comm,
                "Confidence": avg_conf
            },
            key=lambda x: {
                "Technical": avg_tech,
                "Communication": avg_comm,
                "Confidence": avg_conf
            }[x]
        )
        st.success(
            f"Strongest Area: {best_area}"
        )
        st.warning(
            f"Needs Improvement: {weakest_area}"
        )
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

        fig = create_score_trend_chart(
            trend_df
        )
        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Multi line chart
        st.subheader("📊 Skill Score Trends")

        multi_fig = create_skill_trend_chart(
            trend_df
        )

        st.plotly_chart(
            multi_fig,
            use_container_width=True
        )

    # INTERVIEW STATS
    st.divider()
    st.subheader("Interview Statistics")

    if not records:
        st.info(
            "📭 No interview statistics available."
        )
    else:
        stat1, stat2 = st.columns(2)
        with stat1:
            st.metric("Attempted Questions", stats.get("attempted_questions", 0))
        with stat2:
            st.metric("Skipped Questions", stats.get("skipped_questions", 0))
    
    st.divider()
    st.subheader("📊 Interview Comparison")
    
    if len(records) < 2:
        st.info(
            "📭 At least 2 interviews are required for comparison."
        )
    else:
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