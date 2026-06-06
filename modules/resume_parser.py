from PyPDF2 import PdfReader
from docx import Document
import re


# ==========================================================
# RESUME TEXT EXTRACTION
# ==========================================================

def extract_resume_text(uploaded_file):

    try:

        file_name = uploaded_file.name.lower()

        extracted_text = ""

        # ==================================================
        # PDF
        # ==================================================

        if file_name.endswith(".pdf"):

            reader = PdfReader(uploaded_file)

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:

                    extracted_text += (
                        page_text + "\n"
                    )

        # ==================================================
        # DOCX
        # ==================================================

        elif file_name.endswith(".docx"):

            document = Document(
                uploaded_file
            )

            for paragraph in document.paragraphs:

                extracted_text += (
                    paragraph.text + "\n"
                )

        # ==================================================
        # TXT
        # ==================================================

        elif file_name.endswith(".txt"):

            extracted_text = (
                uploaded_file.read()
                .decode("utf-8")
            )

        else:

            return (
                "Unsupported file format. "
                "Upload PDF, DOCX or TXT."
            )

        extracted_text = extracted_text.strip()

        if not extracted_text:

            return (
                "No text found in resume."
            )

        return extracted_text

    except Exception as e:

        return (
            f"Resume Parsing Error:\n"
            f"{str(e)}"
        )


# ==========================================================
# EMAIL EXTRACTION
# ==========================================================

def extract_email(resume_text):

    try:

        match = re.search(

            r"[A-Za-z0-9._%+-]+"
            r"@[A-Za-z0-9.-]+"
            r"\.[A-Za-z]{2,}",

            resume_text
        )

        if match:

            return match.group()

    except Exception:
        pass

    return "Not Found"


# ==========================================================
# PHONE EXTRACTION
# ==========================================================

def extract_phone(resume_text):

    try:

        patterns = [

            r"(\+91[-\s]?)?[6-9]\d{9}",

            r"\+?\d{1,3}[-\s]?\d{10}",

            r"\d{10}"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                resume_text
            )

            if match:

                return match.group()

    except Exception:
        pass

    return "Not Found"


# ==========================================================
# NAME EXTRACTION
# ==========================================================

def extract_name(resume_text):

    try:

        lines = [

            line.strip()

            for line in resume_text.split("\n")

            if line.strip()
        ]

        if lines:

            first_line = lines[0]

            if len(first_line) < 50:

                return first_line

    except Exception:
        pass

    return "Not Found"


# ==========================================================
# PROJECT EXTRACTION
# ==========================================================

def extract_projects(resume_text):

    projects = []

    try:

        patterns = [

            r"projects?(.*?)(education|skills|certifications|experience|$)",

            r"academic projects?(.*?)(education|skills|certifications|experience|$)",

            r"project:(.*?)(education|skills|certifications|experience|$)"
        ]

        for pattern in patterns:

            matches = re.findall(

                pattern,

                resume_text,

                re.IGNORECASE |
                re.DOTALL
            )

            for match in matches:

                section = match[0]

                lines = section.split("\n")

                for line in lines:

                    line = line.strip()

                    if len(line) > 5:

                        projects.append(
                            line
                        )

    except Exception:
        pass

    projects = list(set(projects))

    return projects[:20]


# ==========================================================
# SKILL EXTRACTION
# ==========================================================

def extract_skills_from_resume(
        resume_text
):

    skill_database = [

        # Programming

        "Python",
        "Java",
        "C",
        "C++",
        "JavaScript",
        "TypeScript",
        "PHP",

        # Web

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
        "FastAPI",
        "Streamlit",

        # Database

        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",
        "SQLite",

        # AI

        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "NLP",
        "TensorFlow",
        "PyTorch",
        "Keras",
        "Scikit-learn",
        "OpenCV",
        "Generative AI",
        "LangChain",
        "LLM",

        # Data Science

        "Pandas",
        "NumPy",
        "Matplotlib",
        "Seaborn",

        # Cloud

        "AWS",
        "Azure",
        "GCP",
        "Google Cloud",
        "Firebase",

        # Tools

        "Git",
        "GitHub",
        "Docker",
        "Linux",
        "Postman"
    ]

    detected = []

    try:

        lower_text = resume_text.lower()

        for skill in skill_database:

            if skill.lower() in lower_text:

                detected.append(
                    skill
                )

    except Exception:
        pass

    return sorted(
        list(set(detected))
    )


# ==========================================================
# RESUME DETAILS
# ==========================================================

def extract_resume_details(
        resume_text
):

    details = {

        "name":
            extract_name(
                resume_text
            ),

        "email":
            extract_email(
                resume_text
            ),

        "phone":
            extract_phone(
                resume_text
            ),

        "skills":
            extract_skills_from_resume(
                resume_text
            ),

        "projects":
            extract_projects(
                resume_text
            ),

        "resume_text":
            resume_text
    }

    return details


# ==========================================================
# RESUME SUMMARY
# ==========================================================

def generate_resume_summary(
        resume_text
):

    details = extract_resume_details(
        resume_text
    )

    return {

        "name":
            details["name"],

        "email":
            details["email"],

        "phone":
            details["phone"],

        "skills_count":
            len(
                details["skills"]
            ),

        "project_count":
            len(
                details["projects"]
            ),

        "skills":
            details["skills"],

        "projects":
            details["projects"]
    }


# ==========================================================
# VALIDATION
# ==========================================================

def validate_resume(
        resume_text
):

    if not resume_text:
        return False

    if len(
        resume_text.strip()
    ) < 50:

        return False

    return True