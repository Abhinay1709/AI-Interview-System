import json
import re

def export_history(records):

    report = ""

    report += (
        "AI INTERVIEW PREPARATION SYSTEM\n"
    )

    report += (
        "COMPLETE INTERVIEW HISTORY\n"
    )

    report += (
        "=" * 80 + "\n\n"
    )

    if not records:

        report += (
            "No interview history found.\n"
        )

        return report

    for record in records:

        interview_id = record[0]

        interview_date = record[1]

        questions_json = record[2]

        answers_json = record[3]

        evaluation = record[4]

        try:
            # Fixing bug that breaks older corrupted "null" databases
            questions = json.loads(questions_json) if questions_json and questions_json.strip() not in ['null', ''] else []
            answers = json.loads(answers_json) if answers_json and answers_json.strip() not in ['null', ''] else {}
            
        except Exception:

            questions = []

            answers = {}

        report += (
            f"INTERVIEW #{interview_id}\n"
        )

        report += (
            f"Date: {interview_date}\n"
        )

        report += (
            "-" * 80 + "\n\n"
        )

        report += (
            "QUESTIONS, ANSWERS & FEEDBACK\n\n"
        )

        for index, question in enumerate(
            questions,
            start=1
        ):

            answer = answers.get(
                question,
                "No Answer"
            )

            q_score = "N/A"
            model_answer = "Not available for this record."
            
            if evaluation:
                sm = re.search(rf"Question {index} Score:\s*(.*?/10)", evaluation, re.IGNORECASE)
                if sm: 
                    q_score = sm.group(1)
                
                am = re.search(rf"Question {index} Score:.*?Model Answer:\s*(.*?)(?=\nQuestion \d+ Score|\nTechnical Score|\nCommunication Score|\nQuestions Attempted|\Z)", evaluation, re.DOTALL | re.IGNORECASE)
                if am: 
                    model_answer = am.group(1).strip()

            report += (
                f"Question {index}\n"
            )

            report += (
                f"{question}\n\n"
            )

            report += (
                "Your Answer:\n"
            )

            report += (
                f"{answer}\n\n"
            )

            report += (
                f"Score: {q_score}\n"
            )
            
            report += (
                "Correct/Model Answer:\n"
            )
            
            report += (
                f"{model_answer}\n\n"
            )
            
            report += (
                "-" * 50 + "\n\n"
            )

        report += (
            "OVERALL EVALUATION\n\n"
        )

        report += (
            evaluation or "No evaluation available."
        )

        report += (
            "\n\n"
        )

        report += (
            "=" * 80
        )

        report += (
            "\n\n"
        )

    return report