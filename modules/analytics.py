import re


def calculate_statistics(records):

    total_interviews = len(records)

    technical_scores = []
    communication_scores = []
    confidence_scores = []
    overall_scores = []

    for record in records:

        try:

            evaluation = record[4]

            technical = extract_score(
                evaluation,
                "Technical Score"
            )

            communication = extract_score(
                evaluation,
                "Communication Score"
            )

            confidence = extract_score(
                evaluation,
                "Confidence Score"
            )

            if technical > 0:

                technical_scores.append(
                    technical
                )

            if communication > 0:

                communication_scores.append(
                    communication
                )

            if confidence > 0:

                confidence_scores.append(
                    confidence
                )

            if (
                technical > 0
                and communication > 0
                and confidence > 0
            ):

                overall = round(
                    (
                        technical
                        + communication
                        + confidence
                    ) / 3,
                    1
                )

                overall_scores.append(
                    overall
                )

        except Exception:

            continue

    stats = {

        "total_interviews":
            total_interviews,

        "average_technical":
            calculate_average(
                technical_scores
            ),

        "average_communication":
            calculate_average(
                communication_scores
            ),

        "average_confidence":
            calculate_average(
                confidence_scores
            ),

        "average_overall":
            calculate_average(
                overall_scores
            ),

        "best_score":
            max(
                overall_scores,
                default=0
            ),

        "worst_score":
            min(
                overall_scores,
                default=0
            )
    }

    return stats


def extract_score(
    evaluation_text,
    score_name
):

    try:

        pattern = (
            rf"{score_name}:\s*(\d+)"
        )

        match = re.search(
            pattern,
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


def calculate_average(
    scores
):

    if len(scores) == 0:

        return 0

    return round(

        sum(scores)
        /
        len(scores),

        2
    )