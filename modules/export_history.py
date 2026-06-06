import json
import re
import pandas as pd


# ==========================================================
# SAFE EXTRACT
# ==========================================================

def safe_extract(
        pattern,
        text,
        default="N/A"
):

    try:

        match = re.search(
            pattern,
            str(text),
            re.IGNORECASE | re.DOTALL
        )

        if match:

            value = match.group(1).strip()

            if value:
                return value

    except Exception:
        pass

    return default


# ==========================================================
# QUESTION SCORE
# ==========================================================

def extract_question_score(
        evaluation,
        question_number
):

    try:

        match = re.search(

            rf"Question\s+{question_number}\s+Score:\s*(\d+\/10)",

            evaluation,

            re.IGNORECASE
        )

        if match:
            return match.group(1)

    except Exception:
        pass

    return "0/10"


# ==========================================================
# MODEL ANSWER
# ==========================================================

def extract_model_answer(
        evaluation,
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

            evaluation,

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

def extract_feedback(
        evaluation,
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

            evaluation,

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
# COMPLETION %
# ==========================================================

def calculate_completion(
        answered,
        total_questions
):

    try:

        if total_questions <= 0:
            return 0

        return round(

            (
                answered /
                total_questions
            ) * 100,

            2
        )

    except Exception:
        return 0


# ==========================================================
# EXPORT HISTORY
# ==========================================================

def export_history_to_excel(
        records,
        output_file="Interview_History.xlsx"
):

    rows = []

    # ======================================================
    # NO RECORDS
    # ======================================================

    if not records:

        df = pd.DataFrame(columns=[

            "Interview ID",
            "Interview Date",

            "Question",
            "My Answer",

            "Question Score",
            "Model Answer",
            "Feedback",

            "Technical Score",
            "Communication Score",
            "Confidence Score",
            "Overall Score",

            "Answered Questions",
            "Skipped Questions",
            "Completion %",

            "Strengths",
            "Weaknesses",
            "Suggestions"
        ])

        df.to_excel(
            output_file,
            index=False
        )

        return output_file

    # ======================================================
    # PROCESS RECORDS
    # ======================================================

    for record in records:

        try:

            interview_id = record[0]
            interview_date = record[1]

            questions_json = record[2]
            answers_json = record[3]

            evaluation = record[4]

            technical_score = record[5]
            communication_score = record[6]
            confidence_score = record[7]
            overall_score = record[8]

            total_questions = record[9]
            answered_questions = record[10]
            skipped_questions = record[11]

            completion_percentage = record[12]

            strengths = record[13]
            weaknesses = record[14]
            suggestions = record[15]

            try:

                questions = json.loads(
                    questions_json
                )

            except Exception:

                questions = []

            try:

                answers = json.loads(
                    answers_json
                )

            except Exception:

                answers = {}

            # ==========================================
            # QUESTION ROWS
            # ==========================================

            for index, question in enumerate(
                    questions,
                    start=1
            ):

                answer = answers.get(
                    question,
                    "No Answer"
                )

                question_score = (
                    extract_question_score(
                        evaluation,
                        index
                    )
                )

                model_answer = (
                    extract_model_answer(
                        evaluation,
                        index
                    )
                )

                feedback = (
                    extract_feedback(
                        evaluation,
                        index
                    )
                )

                rows.append({

                    "Interview ID":
                        interview_id,

                    "Interview Date":
                        interview_date,

                    "Question":
                        question,

                    "My Answer":
                        answer,

                    "Question Score":
                        question_score,

                    "Model Answer":
                        model_answer,

                    "Feedback":
                        feedback,

                    "Technical Score":
                        technical_score,

                    "Communication Score":
                        communication_score,

                    "Confidence Score":
                        confidence_score,

                    "Overall Score":
                        overall_score,

                    "Answered Questions":
                        answered_questions,

                    "Skipped Questions":
                        skipped_questions,

                    "Completion %":
                        completion_percentage,

                    "Strengths":
                        strengths,

                    "Weaknesses":
                        weaknesses,

                    "Suggestions":
                        suggestions
                })

        except Exception:
            continue

    # ======================================================
    # CREATE DATAFRAME
    # ======================================================

    df = pd.DataFrame(rows)

    # ======================================================
    # SAVE EXCEL
    # ======================================================

    with pd.ExcelWriter(
            output_file,
            engine="openpyxl"
    ) as writer:

        df.to_excel(

            writer,

            sheet_name="Interview History",

            index=False
        )

        worksheet = writer.sheets[
            "Interview History"
        ]

        # ==============================================
        # AUTO COLUMN WIDTH
        # ==============================================

        for column in worksheet.columns:

            max_length = 0

            column_letter = (
                column[0].column_letter
            )

            for cell in column:

                try:

                    if cell.value:

                        max_length = max(

                            max_length,

                            len(
                                str(cell.value)
                            )
                        )

                except Exception:
                    pass

            worksheet.column_dimensions[
                column_letter
            ].width = min(
                max_length + 5,
                60
            )

    return output_file