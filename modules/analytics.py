import statistics


# ==========================================================
# SAFE AVERAGE
# ==========================================================

def safe_average(values):

    values = [
        float(v)
        for v in values
        if v is not None
    ]

    if not values:
        return 0

    return round(
        sum(values) / len(values),
        2
    )


# ==========================================================
# SAFE MAX
# ==========================================================

def safe_max(values):

    values = [
        float(v)
        for v in values
        if v is not None
    ]

    if not values:
        return 0

    return round(max(values), 2)


# ==========================================================
# SAFE MIN
# ==========================================================

def safe_min(values):

    values = [
        float(v)
        for v in values
        if v is not None
    ]

    if not values:
        return 0

    return round(min(values), 2)


# ==========================================================
# MAIN STATISTICS
# ==========================================================

def calculate_statistics(records):

    stats = {

        "total_interviews": 0,

        "average_technical": 0,
        "average_communication": 0,
        "average_confidence": 0,
        "average_overall": 0,

        "best_score": 0,
        "worst_score": 0,

        "attempted_questions": 0,
        "skipped_questions": 0,

        "completion_rate": 0
    }

    if not records:
        return stats

    technical_scores = []
    communication_scores = []
    confidence_scores = []
    overall_scores = []

    attempted_questions = 0
    skipped_questions = 0

    for record in records:

        try:

            technical_scores.append(
                float(record[5] or 0)
            )

            communication_scores.append(
                float(record[6] or 0)
            )

            confidence_scores.append(
                float(record[7] or 0)
            )

            overall_scores.append(
                float(record[8] or 0)
            )

            attempted_questions += int(
                record[10] or 0
            )

            skipped_questions += int(
                record[11] or 0
            )

        except Exception:
            continue

    total_questions = (
        attempted_questions +
        skipped_questions
    )

    completion_rate = 0

    if total_questions > 0:

        completion_rate = round(

            (
                attempted_questions /
                total_questions
            ) * 100,

            2
        )

    stats = {

        "total_interviews":
            len(records),

        "average_technical":
            safe_average(
                technical_scores
            ),

        "average_communication":
            safe_average(
                communication_scores
            ),

        "average_confidence":
            safe_average(
                confidence_scores
            ),

        "average_overall":
            safe_average(
                overall_scores
            ),

        "best_score":
            safe_max(
                overall_scores
            ),

        "worst_score":
            safe_min(
                overall_scores
            ),

        "attempted_questions":
            attempted_questions,

        "skipped_questions":
            skipped_questions,

        "completion_rate":
            completion_rate
    }

    return stats


# ==========================================================
# DASHBOARD METRICS
# ==========================================================

def get_dashboard_metrics(records):

    stats = calculate_statistics(
        records
    )

    return {

        "Total Interviews":
            stats[
                "total_interviews"
            ],

        "Average Technical Score":
            f"{stats['average_technical']}/10",

        "Average Communication Score":
            f"{stats['average_communication']}/10",

        "Average Confidence Score":
            f"{stats['average_confidence']}/10",

        "Average Overall Score":
            f"{stats['average_overall']}/10",

        "Best Score":
            f"{stats['best_score']}/10",

        "Worst Score":
            f"{stats['worst_score']}/10",

        "Attempted Questions":
            stats[
                "attempted_questions"
            ],

        "Skipped Questions":
            stats[
                "skipped_questions"
            ],

        "Completion Rate":
            f"{stats['completion_rate']}%"
    }


# ==========================================================
# ADVANCED ANALYTICS
# ==========================================================

def get_advanced_statistics(records):

    stats = calculate_statistics(
        records
    )

    overall_scores = []

    for record in records:

        try:

            overall_scores.append(
                float(record[8] or 0)
            )

        except Exception:
            pass

    score_variance = 0

    if len(overall_scores) > 1:

        try:

            score_variance = round(

                statistics.variance(
                    overall_scores
                ),

                2
            )

        except Exception:

            score_variance = 0

    return {

        **stats,

        "score_variance":
            score_variance,

        "highest_score":
            safe_max(
                overall_scores
            ),

        "lowest_score":
            safe_min(
                overall_scores
            )
    }


# ==========================================================
# INTERVIEW SUMMARY
# ==========================================================

def get_interview_summary(records):

    stats = calculate_statistics(
        records
    )

    return {

        "total_interviews":
            stats[
                "total_interviews"
            ],

        "best_score":
            stats[
                "best_score"
            ],

        "worst_score":
            stats[
                "worst_score"
            ],

        "average_score":
            stats[
                "average_overall"
            ],

        "completion_rate":
            stats[
                "completion_rate"
            ]
    }


# ==========================================================
# SCORE TREND
# ==========================================================

def get_score_trend(records):

    trend = []

    for record in records:

        try:

            trend.append({

                "interview_id":
                    record[0],

                "date":
                    record[1],

                "technical":
                    record[5],

                "communication":
                    record[6],

                "confidence":
                    record[7],

                "overall":
                    record[8]
            })

        except Exception:
            continue

    return trend