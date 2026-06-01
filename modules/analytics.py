def calculate_statistics(records):

    total_interviews = len(records)

    total_score = 0

    evaluated_count = 0

    for record in records:

        evaluation = record[3]

        try:

            lines = evaluation.split("\n")

            for line in lines:

                if "Technical Score:" in line:

                    score = int(
                        line.split(":")[1]
                        .replace("/10", "")
                        .strip()
                    )

                    total_score += score

                    evaluated_count += 1

        except:
            pass

    average_score = 0

    if evaluated_count > 0:

        average_score = round(
            total_score / evaluated_count,
            2
        )

    return {
        "total_interviews": total_interviews,
        "average_score": average_score
    }