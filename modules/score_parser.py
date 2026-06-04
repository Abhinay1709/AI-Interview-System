import re


def extract_scores(evaluation_text):

    scores = {
        "technical": 0,
        "communication": 0,
        "confidence": 0,
        "overall": 0,
        "attempted": 0,
        "total_questions": 0,
        "skipped": 0,
        "question_scores": {}      # NEW: individual per-question scores
    }

    try:

        technical_match = re.search(
            r"Technical Score:\s*(\d+)",
            evaluation_text,
            re.IGNORECASE
        )

        communication_match = re.search(
            r"Communication Score:\s*(\d+)",
            evaluation_text,
            re.IGNORECASE
        )

        confidence_match = re.search(
            r"Confidence Score:\s*(\d+)",
            evaluation_text,
            re.IGNORECASE
        )

        attempted_match = re.search(
            r"Questions Attempted:\s*(\d+)\/(\d+)",
            evaluation_text,
            re.IGNORECASE
        )

        skipped_match = re.search(
            r"Questions Skipped:\s*(\d+)\/(\d+)",
            evaluation_text,
            re.IGNORECASE
        )

        # NEW: match "Question N Score: X/10" or "Question N Score: X"
        # (won't clash with "Technical Score" / "Communication Score"
        #  because those don't start with "Question \d+")
        question_score_matches = re.findall(
            r"Question\s+(\d+)\s+Score:\s*(\d+)",
            evaluation_text,
            re.IGNORECASE
        )

        if technical_match:
            scores["technical"] = int(
                technical_match.group(1)
            )

        if communication_match:
            scores["communication"] = int(
                communication_match.group(1)
            )

        if confidence_match:
            scores["confidence"] = int(
                confidence_match.group(1)
            )

        if attempted_match:
            scores["attempted"] = int(
                attempted_match.group(1)
            )
            scores["total_questions"] = int(
                attempted_match.group(2)
            )

        if skipped_match:
            scores["skipped"] = int(
                skipped_match.group(1)
            )

        # Build individual question scores dict
        for q_num, q_score in question_score_matches:
            scores["question_scores"][
                f"Question {q_num}"
            ] = int(q_score)

        scores["overall"] = round(
            (
                scores["technical"]
                + scores["communication"]
                + scores["confidence"]
            ) / 3,
            1
        )

    except Exception:
        pass

    return scores