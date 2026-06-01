import re


def extract_scores(evaluation_text):

    scores = {
        "technical": 0,
        "communication": 0,
        "confidence": 0,
        "overall": 0
    }

    try:

        technical = re.search(
            r"Technical Score:\s*(\d+)",
            evaluation_text,
            re.IGNORECASE
        )

        communication = re.search(
            r"Communication Score:\s*(\d+)",
            evaluation_text,
            re.IGNORECASE
        )

        confidence = re.search(
            r"Confidence Score:\s*(\d+)",
            evaluation_text,
            re.IGNORECASE
        )

        if technical:
            scores["technical"] = int(
                technical.group(1)
            )

        if communication:
            scores["communication"] = int(
                communication.group(1)
            )

        if confidence:
            scores["confidence"] = int(
                confidence.group(1)
            )

        scores["overall"] = round(
            (
                scores["technical"]
                + scores["communication"]
                + scores["confidence"]
            ) / 3,
            1
        )

    except:
        pass

    return scores