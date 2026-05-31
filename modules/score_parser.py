import re


def extract_scores(evaluation_text):
    """
    Extract scores from AI evaluation text.

    Parameters:
        evaluation_text (str)

    Returns:
        dict
    """

    scores = {
        "technical": 0,
        "communication": 0,
        "confidence": 0
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

    except Exception:

        pass

    return scores