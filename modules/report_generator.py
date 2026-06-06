import re
from datetime import datetime


# ==========================================================
# SAFE EXTRACT
# ==========================================================

def safe_extract(
        pattern,
        text,
        default="Not Available"
):

    try:

        match = re.search(
            pattern,
            str(text),
            re.IGNORECASE | re.DOTALL
        )

        if match:

            value = match.group(1).strip()

            if value:
                return value

    except Exception:
        pass

    return default


# ==========================================================
# QUESTION SCORE
# ==========================================================

def extract_question_score(
        evaluation_text,
        question_number
):

    return safe_extract(

        rf"Question\s+{question_number}\s+Score:\s*(\d+\/10)",

        evaluation_text,

        "0/10"
    )


# ==========================================================
# MODEL ANSWER
# ==========================================================

def extract_model_answer(
        evaluation_text,
        question_number
):

    try:

        pattern = (

            rf"Question\s+{question_number}\s+Score:.*?"

            rf"Model Answer:\s*(.*?)"

            rf"Feedback:"
        )

        match = re.search(

            pattern,

            evaluation_text,

            re.IGNORECASE |
            re.DOTALL
        )

        if match:

            return match.group(
                1
            ).strip()

    except Exception:
        pass

    return "Not Available"


# ==========================================================
# FEEDBACK
# ==========================================================

def extract_feedback(
        evaluation_text,
        question_number
):

    try:

        pattern = (

            rf"Question\s+{question_number}\s+Score:.*?"

            rf"Feedback:\s*(.*?)"

            rf"(Question\s+\d+\s+Score:|Technical Score:)"
        )

        match = re.search(

            pattern,

            evaluation_text,

            re.IGNORECASE |
            re.DOTALL
        )

        if match:

            return match.group(
                1
            ).strip()

    except Exception:
        pass

    return "Not Available"


# ==========================================================
# FULL REPORT GENERATOR
# ==========================================================

def generate_full_report(
        questions,
        answers,
        evaluation
):

    report = ""

    # ======================================================
    # HEADER
    # ======================================================

    report += "=" * 80 + "\n"
    report += "AI INTERVIEW PREPARATION SYSTEM REPORT\n"
    report += "=" * 80 + "\n\n"

    report += (
        f"Interview Date : "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    )

    # ======================================================
    # OVERALL SCORES
    # ======================================================

    technical_score = safe_extract(
        r"Technical Score:\s*(.*?/10)",
        evaluation
    )

    communication_score = safe_extract(
        r"Communication Score:\s*(.*?/10)",
        evaluation
    )

    confidence_score = safe_extract(
        r"Confidence Score:\s*(.*?/10)",
        evaluation
    )

    overall_score = safe_extract(
        r"Overall Score:\s*(.*?/10)",
        evaluation
    )

    attempted_questions = safe_extract(
        r"Questions Attempted:\s*(.*)",
        evaluation,
        "0"
    )

    skipped_questions = safe_extract(
        r"Questions Skipped:\s*(.*)",
        evaluation,
        "0"
    )

    # ======================================================
    # COMPLETION %
    # ======================================================

    completion_percentage = "0"

    try:

        attempted_match = re.search(
            r"Questions Attempted:\s*(\d+)\/(\d+)",
            evaluation,
            re.IGNORECASE
        )

        if attempted_match:

            attempted = int(
                attempted_match.group(1)
            )

            total = int(
                attempted_match.group(2)
            )

            if total > 0:

                completion_percentage = str(
                    round(
                        (
                            attempted /
                            total
                        ) * 100,
                        2
                    )
                )

    except Exception:
        pass

    report += "OVERALL EVALUATION\n"
    report += "-" * 50 + "\n"

    report += (
        f"Technical Score      : {technical_score}\n"
    )

    report += (
        f"Communication Score  : {communication_score}\n"
    )

    report += (
        f"Confidence Score     : {confidence_score}\n"
    )

    report += (
        f"Overall Score        : {overall_score}\n"
    )

    report += (
        f"Answered Questions   : {attempted_questions}\n"
    )

    report += (
        f"Skipped Questions    : {skipped_questions}\n"
    )

    report += (
        f"Completion Percentage: "
        f"{completion_percentage}%\n\n"
    )

    # ======================================================
    # QUESTION ANALYSIS
    # ======================================================

    report += "=" * 80 + "\n"
    report += "QUESTION-WISE ANALYSIS\n"
    report += "=" * 80 + "\n\n"

    if not questions:

        report += "No Questions Found.\n\n"

    else:

        for index, question in enumerate(
                questions,
                start=1
        ):

            answer = answers.get(
                question,
                "No Answer"
            )

            score = extract_question_score(
                evaluation,
                index
            )

            model_answer = extract_model_answer(
                evaluation,
                index
            )

            feedback = extract_feedback(
                evaluation,
                index
            )

            report += (
                f"QUESTION {index}\n"
            )

            report += "-" * 60 + "\n\n"

            report += (
                f"Question:\n"
                f"{question}\n\n"
            )

            report += (
                f"My Answer:\n"
                f"{answer}\n\n"
            )

            report += (
                f"Question Score:\n"
                f"{score}\n\n"
            )

            report += (
                f"Expected / Model Answer:\n"
                f"{model_answer}\n\n"
            )

            report += (
                f"Feedback:\n"
                f"{feedback}\n\n"
            )

    # ======================================================
    # STRENGTHS
    # ======================================================

    strengths = safe_extract(

        r"Strengths:(.*?)Weaknesses:",

        evaluation,

        "Not Available"
    )

    report += "=" * 80 + "\n"
    report += "STRENGTHS\n"
    report += "=" * 80 + "\n\n"

    report += strengths + "\n\n"

    # ======================================================
    # WEAKNESSES
    # ======================================================

    weaknesses = safe_extract(

        r"Weaknesses:(.*?)Suggestions:",

        evaluation,

        "Not Available"
    )

    report += "=" * 80 + "\n"
    report += "WEAKNESSES\n"
    report += "=" * 80 + "\n\n"

    report += weaknesses + "\n\n"

    # ======================================================
    # SUGGESTIONS
    # ======================================================

    suggestions = safe_extract(

        r"Suggestions:(.*)",

        evaluation,

        "Not Available"
    )

    report += "=" * 80 + "\n"
    report += "SUGGESTIONS\n"
    report += "=" * 80 + "\n\n"

    report += suggestions + "\n\n"

    # ======================================================
    # RAW EVALUATION
    # ======================================================

    report += "=" * 80 + "\n"
    report += "RAW EVALUATION DATA\n"
    report += "=" * 80 + "\n\n"

    report += str(evaluation)

    report += "\n\n"

    report += "=" * 80 + "\n"
    report += "END OF REPORT\n"
    report += "=" * 80 + "\n"

    return report