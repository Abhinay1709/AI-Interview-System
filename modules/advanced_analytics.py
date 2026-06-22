def calculate_improvement(records):

    if len(records) < 2:
        return 0

    first_score = float(
        records[-1][8] or 0
    )

    latest_score = float(
        records[0][8] or 0
    )

    return round(
        latest_score - first_score,
        2
    )


def calculate_consistency(records):

    if not records:
        return 0

    scores = [

        float(record[8] or 0)

        for record in records
    ]

    avg = sum(scores) / len(scores)

    deviation = sum(
        abs(score - avg)
        for score in scores
    ) / len(scores)

    consistency = max(
        0,
        100 - (deviation * 10)
    )

    return round(
        consistency,
        2
    )


def strongest_area(stats):

    areas = {

        "Technical":
        stats.get(
            "average_technical",
            0
        ),

        "Communication":
        stats.get(
            "average_communication",
            0
        ),

        "Confidence":
        stats.get(
            "average_confidence",
            0
        )
    }

    return max(
        areas,
        key=areas.get
    )


def weakest_area(stats):

    areas = {

        "Technical":
        stats.get(
            "average_technical",
            0
        ),

        "Communication":
        stats.get(
            "average_communication",
            0
        ),

        "Confidence":
        stats.get(
            "average_confidence",
            0
        )
    }

    return min(
        areas,
        key=areas.get
    )