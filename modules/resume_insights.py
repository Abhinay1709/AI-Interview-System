def generate_resume_insights(
        resume_details,
        ats_result
):

    strengths = []

    improvements = []

    recommendations = []

    skills = resume_details.get(
        "skills",
        []
    )

    projects = resume_details.get(
        "projects",
        []
    )

    # ==========================
    # SKILLS
    # ==========================

    if len(skills) >= 5:

        strengths.append(
            "Strong technical skill set"
        )

    else:

        improvements.append(
            "Limited technical skills listed"
        )

        recommendations.append(
            "Add more relevant technical skills"
        )

    # ==========================
    # PROJECTS
    # ==========================

    if len(projects) >= 2:

        strengths.append(
            "Multiple projects showcased"
        )

    else:

        improvements.append(
            "Few projects listed"
        )

        recommendations.append(
            "Add more projects to demonstrate experience"
        )

    # ==========================
    # ATS MISSING ITEMS
    # ==========================

    for item in ats_result["missing"]:

        improvements.append(
            f"{item} missing"
        )

    # ==========================
    # ATS SUGGESTIONS
    # ==========================

    recommendations.extend(
        ats_result["suggestions"]
    )

    return {

        "strengths":
            strengths,

        "improvements":
            improvements,

        "recommendations":
            recommendations
    }