import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


# ==========================================
# RADAR CHART
# ==========================================

def create_radar_chart(
    technical,
    communication,
    confidence
):

    project_knowledge = round(
        (technical + confidence) / 2,
        1
    )

    problem_solving = round(
        (technical + communication) / 2,
        1
    )

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

    return fig


# ==========================================
# OVERALL SCORE TREND
# ==========================================

def create_score_trend_chart(
    trend_df
):

    fig = px.line(

        trend_df,

        x="Interview",
        y="Overall",

        markers=True,

        title="Overall Score Trend"

    )

    return fig


# ==========================================
# SKILL TREND
# ==========================================

def create_skill_trend_chart(
    trend_df
):

    fig = px.line(

        trend_df,

        x="Interview",

        y=[
            "Technical",
            "Communication",
            "Confidence"
        ],

        markers=True

    )

    return fig