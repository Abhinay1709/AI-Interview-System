import re


SKILL_DATABASE = {

    "Programming Languages": [

        "Python",
        "Java",
        "C",
        "C++",
        "C#",
        "JavaScript",
        "TypeScript",
        "PHP",
        "Go",
        "Rust",
        "Kotlin",
        "Swift"
    ],

    "Web Development": [

        "HTML",
        "CSS",
        "Bootstrap",
        "React",
        "Angular",
        "Vue",
        "Node.js",
        "Express",
        "Flask",
        "Django",
        "Streamlit",
        "FastAPI",
        "REST API"
    ],

    "Databases": [

        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",
        "SQLite",
        "Oracle",
        "Redis"
    ],

    "AI / ML": [

        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "NLP",
        "Computer Vision",
        "TensorFlow",
        "PyTorch",
        "Keras",
        "OpenCV",
        "Scikit-learn",
        "LLM",
        "Generative AI",
        "LangChain"
    ],

    "Data Analysis": [

        "Pandas",
        "NumPy",
        "Matplotlib",
        "Seaborn",
        "Power BI",
        "Tableau",
        "Excel"
    ],

    "Cloud": [

        "AWS",
        "Azure",
        "Google Cloud",
        "GCP",
        "Firebase"
    ],

    "Tools": [

        "Git",
        "GitHub",
        "Docker",
        "Linux",
        "Jupyter",
        "VS Code",
        "Postman"
    ],

    "Mobile Development": [

        "Android",
        "Flutter",
        "React Native"
    ]
}


def extract_skills(
    resume_text
):

    if not resume_text:

        return []

    detected_skills = []

    resume_text_lower = (
        resume_text.lower()
    )

    for category in SKILL_DATABASE:

        for skill in (
            SKILL_DATABASE[category]
        ):

            if (
                skill.lower()
                in resume_text_lower
            ):

                detected_skills.append(
                    skill
                )

    detected_skills = list(
        set(detected_skills)
    )

    detected_skills.sort()

    return detected_skills


# --------------------------------------------------
# CATEGORY WISE SKILLS
# --------------------------------------------------

def extract_skills_by_category(
    resume_text
):

    categorized_skills = {}

    if not resume_text:

        return categorized_skills

    resume_text_lower = (
        resume_text.lower()
    )

    for category, skills in (
        SKILL_DATABASE.items()
    ):

        found_skills = []

        for skill in skills:

            if (
                skill.lower()
                in resume_text_lower
            ):

                found_skills.append(
                    skill
                )

        if found_skills:

            categorized_skills[
                category
            ] = sorted(
                list(
                    set(
                        found_skills
                    )
                )
            )

    return categorized_skills


# --------------------------------------------------
# TOTAL SKILLS COUNT
# --------------------------------------------------

def get_total_skills(
    resume_text
):

    skills = extract_skills(
        resume_text
    )

    return len(skills)


# --------------------------------------------------
# RESUME SUMMARY
# --------------------------------------------------

def generate_skill_summary(
    resume_text
):

    categorized_skills = (
        extract_skills_by_category(
            resume_text
        )
    )

    total_skills = (
        get_total_skills(
            resume_text
        )
    )

    return {

        "total_skills":
            total_skills,

        "categorized_skills":
            categorized_skills
    }


# --------------------------------------------------
# TOP SKILLS
# --------------------------------------------------

def get_top_skills(
    resume_text,
    limit=10
):

    skills = extract_skills(
        resume_text
    )

    return skills[:limit]