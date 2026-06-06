import re


# ==========================================================
# SAFE EXTRACT
# ==========================================================

def safe_extract(
        pattern,
        text,
        default=""
):

    try:

        match = re.search(

            pattern,

            str(text),

            re.IGNORECASE |
            re.DOTALL
        )

        if match:

            value = match.group(
                1
            ).strip()

            if value:
                return value

    except Exception:
        pass

    return default


# ==========================================================
# MAIN SCORE EXTRACTION
# ==========================================================

def extract_scores(
        evaluation_text
):

    scores = {

        "technical": 0,

        "communication": 0,

        "confidence": 0,

        "overall": 0,

        "attempted": 0,

        "skipped": 0,

        "total_questions": 0,

        "completion_percentage": 0,

        "question_scores": {},

        "strengths": "",

        "weaknesses": "",

        "suggestions": ""
    }

    try:

        # ==================================================
        # OVERALL SCORES
        # ==================================================

        technical = safe_extract(

            r"Technical Score:\s*(\d+)",

            evaluation_text,

            "0"
        )

        communication = safe_extract(

            r"Communication Score:\s*(\d+)",

            evaluation_text,

            "0"
        )

        confidence = safe_extract(

            r"Confidence Score:\s*(\d+)",

            evaluation_text,

            "0"
        )

        overall = safe_extract(

            r"Overall Score:\s*(\d+)",

            evaluation_text,

            "0"
        )

        scores["technical"] = int(
            technical
        )

        scores["communication"] = int(
            communication
        )

        scores["confidence"] = int(
            confidence
        )

        scores["overall"] = int(
            overall
        )

        # ==================================================
        # ATTEMPTED
        # ==================================================

        attempted_match = re.search(

            r"Questions Attempted:\s*(\d+)\/(\d+)",

            evaluation_text,

            re.IGNORECASE
        )

        if attempted_match:

            scores["attempted"] = int(
                attempted_match.group(1)
            )

            scores["total_questions"] = int(
                attempted_match.group(2)
            )

        # ==================================================
        # SKIPPED
        # ==================================================

        skipped_match = re.search(

            r"Questions Skipped:\s*(\d+)\/(\d+)",

            evaluation_text,

            re.IGNORECASE
        )

        if skipped_match:

            scores["skipped"] = int(
                skipped_match.group(1)
            )

        # ==================================================
        # COMPLETION %
        # ==================================================

        if scores["total_questions"] > 0:

            scores[
                "completion_percentage"
            ] = round(

                (
                    scores["attempted"]
                    /
                    scores["total_questions"]
                ) * 100,

                2
            )

        # ==================================================
        # QUESTION SCORES
        # ==================================================

        question_matches = re.findall(

            r"Question\s+(\d+)\s+Score:\s*(\d+)",

            evaluation_text,

            re.IGNORECASE
        )

        for question_no, score in question_matches:

            scores[
                "question_scores"
            ][
                f"Question {question_no}"
            ] = int(score)

        # ==================================================
        # STRENGTHS
        # ==================================================

        strengths = safe_extract(

            r"Strengths:(.*?)Weaknesses:",

            evaluation_text
        )

        scores["strengths"] = strengths

        # ==================================================
        # WEAKNESSES
        # ==================================================

        weaknesses = safe_extract(

            r"Weaknesses:(.*?)Suggestions:",

            evaluation_text
        )

        scores["weaknesses"] = weaknesses

        # ==================================================
        # SUGGESTIONS
        # ==================================================

        suggestions = safe_extract(

            r"Suggestions:(.*)",

            evaluation_text
        )

        scores["suggestions"] = suggestions

    except Exception:

        pass

    return scores


# ==========================================================
# QUESTION SCORE
# ==========================================================

def get_question_score(
        evaluation_text,
        question_number
):

    try:

        match = re.search(

            rf"Question\s+{question_number}\s+Score:\s*(\d+)",

            evaluation_text,

            re.IGNORECASE
        )

        if match:

            return int(
                match.group(1)
            )

    except Exception:
        pass

    return 0


# ==========================================================
# MODEL ANSWER
# ==========================================================

def get_model_answer(
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

            return (
                match.group(1)
                .strip()
            )

    except Exception:
        pass

    return "Not Available"


# ==========================================================
# FEEDBACK
# ==========================================================

def get_feedback(
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

            return (
                match.group(1)
                .strip()
            )

    except Exception:
        pass

    return "Not Available"


# ==========================================================
# QUESTION ANALYSIS
# ==========================================================

def get_question_analysis(
        evaluation_text,
        question_number
):

    return {

        "score":
            get_question_score(
                evaluation_text,
                question_number
            ),

        "model_answer":
            get_model_answer(
                evaluation_text,
                question_number
            ),

        "feedback":
            get_feedback(
                evaluation_text,
                question_number
            )
    }


# ==========================================================
# ALL QUESTION ANALYSIS
# ==========================================================

def get_all_question_analysis(
        evaluation_text,
        total_questions
):

    analysis = []

    for question_number in range(
            1,
            total_questions + 1
    ):

        analysis.append({

            "question_number":
                question_number,

            "score":
                get_question_score(
                    evaluation_text,
                    question_number
                ),

            "model_answer":
                get_model_answer(
                    evaluation_text,
                    question_number
                ),

            "feedback":
                get_feedback(
                    evaluation_text,
                    question_number
                )
        })

    return analysis