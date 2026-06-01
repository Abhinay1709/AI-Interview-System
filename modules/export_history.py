def export_history(records):
    
    content = "AI Interview History\n\n"

    for record in records:

        content += (
            f"Interview ID: {record[0]}\n\n"
        )

        content += (
            f"Question:\n{record[1]}\n\n"
        )

        content += (
            f"Answer:\n{record[2]}\n\n"
        )

        content += (
            f"Evaluation:\n{record[3]}\n\n"
        )

        content += (
            "=" * 50 + "\n\n"
        )

    return content