def extract_skills(resume_text):
    
    if not resume_text:

        return []

    skill_database = [

        # Programming Languages

        "Python",
        "Java",
        "C",
        "C++",
        "C#",
        "JavaScript",
        "TypeScript",

        # Web Development

        "HTML",
        "CSS",
        "React",
        "Angular",
        "Vue",
        "Node.js",
        "Express",
        "Flask",
        "Django",
        "Streamlit",

        # Databases

        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",
        "SQLite",

        # AI / ML

        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "Data Science",
        "NLP",
        "Computer Vision",
        "TensorFlow",
        "PyTorch",
        "Keras",
        "OpenCV",
        "Scikit-learn",

        # Data Analysis

        "Pandas",
        "NumPy",
        "Matplotlib",
        "Seaborn",
        "Power BI",
        "Tableau",
        "Excel",

        # Cloud

        "AWS",
        "Azure",
        "Google Cloud",

        # Tools

        "Git",
        "GitHub",
        "Docker",
        "Linux",

        # Mobile

        "Android",
        "Flutter",

        # Other

        "REST API",
        "FastAPI"
    ]

    detected_skills = []

    resume_text_lower = (
        resume_text.lower()
    )

    for skill in skill_database:

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