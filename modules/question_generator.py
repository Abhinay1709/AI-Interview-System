import re
import google.generativeai as genai


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
        skills=None,
        projects=None
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

        prompt = f"""
You are a Senior Technical Interviewer.

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

        response = model.generate_content(
            prompt
        )

        generated_text = response.text.strip()

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

    except Exception:

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