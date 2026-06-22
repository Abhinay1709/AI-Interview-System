from modules.skill_gap_analyzer import (
    ROLE_SKILLS
)


# ==========================================
# PLACEMENT PROBABILITY
# ==========================================

def calculate_placement_probability(
    ats_score,
    interview_score
):

    probability = round(

        (
            ats_score +
            (interview_score * 10)
        ) / 2,

        2
    )

    return probability


# ==========================================
# CAREER PATH
# ==========================================

def get_best_career_path(
    skills
):

    scores = {}

    detected = [

        skill.lower()
        for skill in skills
    ]

    for role, role_skills in ROLE_SKILLS.items():

        matched = 0

        for skill in role_skills:

            if skill.lower() in detected:

                matched += 1

        scores[role] = matched

    return max(
        scores,
        key=scores.get
    )


# ==========================================
# LEARNING ROADMAP
# ==========================================

def get_learning_roadmap(
    skills,
    role
):

    detected = [

        skill.lower()
        for skill in skills
    ]

    roadmap = []

    for skill in ROLE_SKILLS.get(
        role,
        []
    ):

        if skill.lower() not in detected:

            roadmap.append(
                skill
            )

    return roadmap[:5]