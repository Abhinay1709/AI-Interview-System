import re


def calculate_ats_score(resume_text):

    score = 0

    strengths = []

    missing = []

    suggestions = []

    # =========================
    # EMAIL
    # =========================

    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    if re.search(email_pattern, resume_text):

        score += 10
        strengths.append("Email Found")

    else:

        missing.append("Email")
        suggestions.append("Add email address")

    # =========================
    # PHONE
    # =========================

    phone_pattern = r"(\+91[-\s]?)?[6-9]\d{9}"

    if re.search(phone_pattern, resume_text):

        score += 10
        strengths.append("Phone Number Found")

    else:

        missing.append("Phone Number")
        suggestions.append("Add phone number")

    # =========================
    # SKILLS
    # =========================

    skills_keywords = [

        "python",
        "java",
        "sql",
        "html",
        "css",
        "machine learning",
        "ai",
        "tensorflow",
        "pytorch"
    ]

    skill_count = 0

    for skill in skills_keywords:

        if skill in resume_text.lower():

            skill_count += 1

    if skill_count >= 3:

        score += 20
        strengths.append("Skills Section Present")

    else:

        missing.append("Skills Section")
        suggestions.append("Add more technical skills")

    # =========================
    # PROJECTS
    # =========================

    if "project" in resume_text.lower():

        score += 20
        strengths.append("Projects Section Present")

    else:

        missing.append("Projects Section")
        suggestions.append("Add academic or personal projects")

    # =========================
    # EDUCATION
    # =========================

    education_keywords = [

        "b.tech",
        "btech",
        "degree",
        "college",
        "university"
    ]

    found = False

    for keyword in education_keywords:

        if keyword in resume_text.lower():

            found = True
            break

    if found:

        score += 15
        strengths.append("Education Section Present")

    else:

        missing.append("Education")
        suggestions.append("Add education details")

    # =========================
    # GITHUB
    # =========================

    if "github.com" in resume_text.lower():

        score += 10
        strengths.append("GitHub Found")

    else:

        missing.append("GitHub")
        suggestions.append("Add GitHub profile")

    # =========================
    # LINKEDIN
    # =========================

    if "linkedin.com" in resume_text.lower():

        score += 10
        strengths.append("LinkedIn Found")

    else:

        missing.append("LinkedIn")
        suggestions.append("Add LinkedIn profile")

    # =========================
    # EXPERIENCE
    # =========================

    experience_keywords = [

        "internship",
        "experience",
        "training"
    ]

    found = False

    for keyword in experience_keywords:

        if keyword in resume_text.lower():

            found = True
            break

    if found:

        score += 5
        strengths.append("Experience Mentioned")

    else:

        suggestions.append("Add internship experience")

    score = min(score, 100)

    return {

        "score": score,

        "strengths": strengths,

        "missing": missing,

        "suggestions": suggestions
    }