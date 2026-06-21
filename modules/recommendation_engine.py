from modules.skill_gap_analyzer import ROLE_SKILLS


def calculate_role_matches(
    detected_skills
):

    results = []

    detected = [
        skill.lower()
        for skill in detected_skills
    ]

    for role, skills in ROLE_SKILLS.items():

        matched = 0

        for skill in skills:

            if skill.lower() in detected:
                matched += 1

        score = round(
            (
                matched /
                len(skills)
            ) * 100,
            2
        )

        results.append(
            {
                "role": role,
                "score": score
            }
        )

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results

def calculate_resume_match(
    detected_skills,
    selected_role
):

    role_skills = ROLE_SKILLS.get(
        selected_role,
        []
    )

    if not role_skills:
        return 0

    matched = 0

    detected = [
        skill.lower()
        for skill in detected_skills
    ]

    for skill in role_skills:

        if skill.lower() in detected:

            matched += 1

    return round(

        (
            matched /
            len(role_skills)
        ) * 100,

        2
    )