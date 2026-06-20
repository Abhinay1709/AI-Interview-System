import json
import re
import pandas as pd


# ==========================================================
# CLEAN TEXT
# ==========================================================

def clean_text(text):

    if not text:
        return ""

    cleaned_lines = []

    for line in str(text).splitlines():

        line = line.strip()

        if not line:
            continue

        line = re.sub(
            r"^[*\-•\s]+",
            "",
            line
        )

        cleaned_lines.append(
            f"• {line}"
        )

    return "\n".join(
        cleaned_lines
    )


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
# AUTO WIDTH
# ==========================================================

def auto_adjust_width(
        worksheet
):

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


# ==========================================================
# EXPORT HISTORY
# ==========================================================

def export_history_to_excel(
        records,
        output_file="Interview_History.xlsx"
):

    summary_rows = []

    # ======================================================
    # NO RECORDS
    # ======================================================

    if not records:

        df = pd.DataFrame(columns=[

            "Interview ID",
            "Interview Date",

            "Technical Score",
            "Communication Score",
            "Confidence Score",
            "Overall Score",

            "Total Questions",
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

            technical_score = record[5]
            communication_score = record[6]
            confidence_score = record[7]
            overall_score = record[8]

            total_questions = record[9]
            answered_questions = record[10]
            skipped_questions = record[11]

            completion_percentage = record[12]

            strengths = clean_text(
                record[13]
            )

            weaknesses = clean_text(
                record[14]
            )

            suggestions = clean_text(
                record[15]
            )

            summary_rows.append({

                "Interview ID":
                    interview_id,

                "Interview Date":
                    interview_date,

                "Technical Score":
                    technical_score,

                "Communication Score":
                    communication_score,

                "Confidence Score":
                    confidence_score,

                "Overall Score":
                    overall_score,

                "Total Questions":
                    total_questions,

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
    # DATAFRAME
    # ======================================================

    summary_df = pd.DataFrame(
        summary_rows
    )

    # ======================================================
    # EXPORT EXCEL
    # ======================================================

    with pd.ExcelWriter(
            output_file,
            engine="openpyxl"
    ) as writer:

        summary_df.to_excel(
            writer,
            sheet_name="Interview Summary",
            index=False
        )

        worksheet = writer.sheets[
            "Interview Summary"
        ]

        auto_adjust_width(
            worksheet
        )

    return output_file