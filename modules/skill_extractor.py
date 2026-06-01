def extract_skills(text):
    
    if not text:
        return []

    skills_database = [

        "Python",
        "Java",
        "C",
        "C++",
        "SQL",
        "MySQL",
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "Flask",
        "Django",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "TensorFlow",
        "PyTorch",
        "Pandas",
        "NumPy",
        "OpenCV",
        "Git",
        "GitHub",
        "Power BI",
        "Excel"
    ]

    detected_skills = []

    for skill in skills_database:

        if skill.lower() in text.lower():

            if skill not in detected_skills:

                detected_skills.append(skill)

    detected_skills.sort()

    return detected_skills