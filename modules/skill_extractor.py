def extract_skills(text):
    """
    Extract predefined skills from resume text.
    """

    skills_database = [

        "Python",
        "Java",
        "C",
        "C++",
        "SQL",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "Data Science",
        "Flask",
        "Django",
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "MongoDB",
        "MySQL",
        "Power BI",
        "Excel",
        "Git",
        "GitHub",
        "TensorFlow",
        "Keras",
        "PyTorch",
        "NumPy",
        "Pandas",
        "OpenCV"
    ]

    detected_skills = []

    for skill in skills_database:

        if skill.lower() in text.lower():
            detected_skills.append(skill)

    return detected_skills