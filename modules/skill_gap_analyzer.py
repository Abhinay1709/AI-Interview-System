# ==================================================
# ROLE SKILLS
# ==================================================

ROLE_SKILLS = {

    "AI Engineer": [

        "python",
        "machine learning",
        "tensorflow",
        "pytorch",
        "deep learning",
        "nlp",
        "computer vision",
        "sql"
    ],

    "ML Engineer": [

        "python",
        "machine learning",
        "tensorflow",
        "pytorch",
        "feature engineering",
        "mlops",
        "sql"
    ],

    "Data Analyst": [

        "sql",
        "excel",
        "power bi",
        "statistics",
        "python",
        "data visualization"
    ],

    "Python Developer": [

        "python",
        "oop",
        "flask",
        "django",
        "api",
        "sql"
    ],

    "Software Engineer": [

        "dsa",
        "oop",
        "dbms",
        "os",
        "computer networks",
        "sql"
    ],

    "Full Stack Developer": [

        "html",
        "css",
        "javascript",
        "react",
        "node",
        "sql"
    ]
}


# ==================================================
# ANALYZER
# ==================================================

def analyze_skill_gap(
        detected_skills,
        target_role
):

    required_skills = ROLE_SKILLS.get(
        target_role,
        []
    )

    detected_lower = [

        skill.lower()
        for skill in detected_skills
    ]

    current_skills = []

    missing_skills = []

    for skill in required_skills:

        if skill in detected_lower:

            current_skills.append(
                skill
            )

        else:

            missing_skills.append(
                skill
            )

    readiness = round(

        (
            len(current_skills)
            /
            max(
                len(required_skills),
                1
            )
        ) * 100,

        2
    )

    return {

        "current_skills":
            current_skills,

        "missing_skills":
            missing_skills,

        "readiness":
            readiness
    }