import re
import google.generativeai as genai

from modules.error_logger import (
    log_error
)
# ==========================================================
# PROJECT EXTRACTION
# ==========================================================

def extract_projects(resume_text):

    if not resume_text:
        return []

    project_patterns = [

        r"projects?(.*?)(education|certification|skills|experience|$)",

        r"project:(.*?)(education|certification|skills|experience|$)",

        r"academic project(.*?)(education|certification|skills|experience|$)"
    ]

    projects = []

    try:

        for pattern in project_patterns:

            matches = re.findall(
                pattern,
                resume_text,
                re.IGNORECASE | re.DOTALL
            )

            for match in matches:

                if isinstance(match, tuple):
                    text = match[0]
                else:
                    text = match

                lines = text.split("\n")

                for line in lines:

                    cleaned = line.strip()

                    if len(cleaned) > 5:
                        projects.append(cleaned)

    except Exception:
        pass

    projects = list(set(projects))

    return projects[:10]


# ==========================================================
# CLEAN QUESTIONS
# ==========================================================

def clean_questions(text):

    questions = []

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        line = re.sub(
            r"^\d+\.\s*",
            "",
            line
        )

        line = re.sub(
            r"^-\s*",
            "",
            line
        )

        if "?" not in line:
            continue

        questions.append(line)

    return questions


# ==========================================================
# FALLBACK QUESTIONS
# ==========================================================

def generate_fallback_questions():

    return [

        # Technical (5)

        "Explain the main technologies mentioned in your resume.",

        "What is the most challenging technical problem you solved?",

        "How do you debug application issues?",

        "What are the advantages of the programming language you use most?",

        "Explain a project architecture you have worked on.",

        # HR (3)

        "Tell me about yourself.",

        "Why should we hire you?",

        "Where do you see yourself in five years?",

        # Project (2)

        "Explain your most important project.",

        "What challenges did you face during project development?"
    ]


# ==========================================================
# GENERATE QUESTIONS
# ==========================================================

def generate_questions(
    resume_text,
    skills,
    projects,
    difficulty="Intermediate",
    job_role="AI Engineer"
):

    try:

        if skills is None:
            skills = []

        if projects is None:
            projects = extract_projects(
                resume_text
            )

        skill_text = ", ".join(skills)

        project_text = "\n".join(projects)

        difficulty_instruction = ""

        if difficulty == "Beginner":

            difficulty_instruction = """
        Generate simple interview questions.

        Focus on:
        - Basic concepts
        - Definitions
        - Fundamental understanding

        Avoid advanced concepts.
        """

        elif difficulty == "Intermediate":

            difficulty_instruction = """
        Generate moderately challenging interview questions.

        Focus on:
        - Practical usage
        - Real-world examples
        - Problem solving
        """

        else:

            difficulty_instruction = """
        Generate advanced interview questions.

        Focus on:
        - Deep technical concepts
        - Optimization
        - System design thinking
        - Advanced problem solving
        """

        role_instruction = ""

        if job_role == "AI Engineer":

            role_instruction = """
        Focus on:

        - Machine Learning
        - Deep Learning
        - Python
        - AI Projects
        - NLP
        """

        elif job_role == "ML Engineer":

            role_instruction = """
        Focus on:

        - Machine Learning
        - Model Training
        - Feature Engineering
        - Scikit-Learn
        - Deployment
        """

        elif job_role == "Data Analyst":

            role_instruction = """
        Focus on:

        - SQL
        - Excel
        - Data Visualization
        - Statistics
        - Power BI
        """

        elif job_role == "Python Developer":

            role_instruction = """
        Focus on:

        - Python
        - OOP
        - APIs
        - Flask
        - Django
        """

        elif job_role == "Software Engineer":

            role_instruction = """
        Focus on:

        - DSA
        - OOP
        - DBMS
        - Operating Systems
        - Computer Networks
        """

        elif job_role == "Full Stack Developer":

            role_instruction = """
        Focus on:

        - HTML
        - CSS
        - JavaScript
        - React
        - Node.js
        - Databases
        """

        prompt = f"""
        


You are a Senior Technical Interviewer.
{difficulty_instruction}
{role_instruction}
Analyze the candidate resume carefully.

================================================

RESUME

{resume_text}

================================================

DETECTED SKILLS

{skill_text}

================================================

PROJECTS

{project_text}

================================================

Generate EXACTLY 10 interview questions.

Distribution:

Technical Questions : 5
HR Questions        : 3
Project Questions   : 2

Rules:

1. Technical questions must be based on:
   - Skills
   - Technologies
   - Programming Languages
   - Databases
   - Frameworks
   - AI/ML tools

2. HR questions must evaluate:
   - Communication
   - Teamwork
   - Leadership
   - Career Goals

3. Project questions must be based on:
   - Resume Projects
   - Internship Projects
   - Academic Projects

Output Rules:

- Exactly 10 questions
- Number them 1 to 10
- No headings
- No explanations
- No answers
- Questions only
"""

        model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        from modules.gemini_helper import (
            generate_with_retry
        )
        response_text = generate_with_retry(
            model,
            prompt
        )
        
        if not response_text:
            raise Exception(
                "Empty Gemini response"
            )

        generated_text = response_text.strip()

        questions = clean_questions(
            generated_text
        )

        if len(questions) > 10:
            questions = questions[:10]

        if len(questions) < 10:

            fallback = generate_fallback_questions()

            while len(questions) < 10:

                questions.append(
                    fallback[
                        len(questions)
                    ]
                )

        return questions

    except Exception as e:
        log_error(e)
        error_message = str(e)
        if "429" in error_message:
            return generate_fallback_questions()
        elif "503" in error_message:
            return generate_fallback_questions()
        elif "timeout" in error_message.lower():
            return generate_fallback_questions()
        else:
            print(
                f"Question Generation Error: {error_message}"
            )
            return generate_fallback_questions()

# ==========================================================
# GENERATE CATEGORY GROUPS
# ==========================================================

def generate_question_groups(
        resume_text,
        skills=None,
        projects=None
):

    questions = generate_questions(
        resume_text,
        skills,
        projects
    )

    grouped = {

        "Technical": questions[:5],

        "HR": questions[5:8],

        "Project": questions[8:10]
    }

    return grouped


# ==========================================================
# VALIDATE QUESTION COUNT
# ==========================================================

def validate_question_count(
        questions
):

    return len(questions) == 10


# ==========================================================
# QUESTION DISTRIBUTION
# ==========================================================

def get_question_distribution():

    return {

        "Technical": 5,

        "HR": 3,

        "Project": 2,

        "Total": 10
    }


# ==========================================================
# QUESTION CATEGORY
# ==========================================================

def get_question_category(index):

    if index < 5:
        return "Technical"

    if index < 8:
        return "HR"

    return "Project"


# ==========================================================
# PROJECT SUMMARY
# ==========================================================

def get_project_summary(
        resume_text
):

    projects = extract_projects(
        resume_text
    )

    return {

        "project_count":
            len(projects),

        "projects":
            projects
    }