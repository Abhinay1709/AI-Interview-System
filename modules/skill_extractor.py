def extract_skills(text):
    """
    Extract skills from resume text using
    predefined skill matching.

    Parameters:
        text (str): Resume text

    Returns:
        list: Detected skills
    """

    if not text:
        return []

    skills_database = [

        # Programming Languages
        "Python",
        "Java",
        "C",
        "C++",
        "C#",
        "JavaScript",
        "TypeScript",
        "PHP",

        # Web Development
        "HTML",
        "CSS",
        "Bootstrap",
        "React",
        "Angular",
        "Vue",
        "Node.js",
        "Express.js",

        # Backend Frameworks
        "Flask",
        "Django",
        "FastAPI",
        "Spring Boot",

        # Databases
        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",
        "SQLite",
        "Oracle",

        # Data Science
        "NumPy",
        "Pandas",
        "Matplotlib",
        "Seaborn",
        "Scikit-learn",

        # AI / ML
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "NLP",
        "Computer Vision",
        "TensorFlow",
        "Keras",
        "PyTorch",
        "OpenCV",

        # Cloud & DevOps
        "AWS",
        "Azure",
        "Google Cloud",
        "Docker",
        "Kubernetes",

        # Tools
        "Git",
        "GitHub",
        "Postman",
        "Power BI",
        "Excel",
        "VS Code",

        # Mobile Development
        "Android",
        "Flutter",
        "React Native"
    ]

    detected_skills = []

    resume_text = text.lower()

    for skill in skills_database:

        if skill.lower() in resume_text:

            if skill not in detected_skills:
                detected_skills.append(skill)

    detected_skills.sort()

    return detected_skills