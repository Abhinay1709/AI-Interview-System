import sqlite3
import json
from datetime import datetime
from modules.answer_evaluator import (
    clean_evaluation_text
)

DB_NAME = "interview_data.db"


# ==========================================================
# CREATE TABLE
# ==========================================================

def create_table():
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interviews (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        interview_date TEXT,

        questions TEXT,
        answers TEXT,
        evaluation TEXT,

        technical_score REAL,
        communication_score REAL,
        confidence_score REAL,
        overall_score REAL,

        total_questions INTEGER,
        answered_questions INTEGER,
        skipped_questions INTEGER,
        completion_percentage REAL,

        strengths TEXT,
        weaknesses TEXT,
        suggestions TEXT
    )
    """)

    conn.commit()

    existing_columns = [

        row[1]

        for row in cursor.execute(
            "PRAGMA table_info(interviews)"
        ).fetchall()
    ]

    required_columns = {

        "technical_score": "REAL",
        "communication_score": "REAL",
        "confidence_score": "REAL",
        "overall_score": "REAL",

        "total_questions": "INTEGER",
        "answered_questions": "INTEGER",
        "skipped_questions": "INTEGER",
        "completion_percentage": "REAL",

        "strengths": "TEXT",
        "weaknesses": "TEXT",
        "suggestions": "TEXT"
    }

    for column_name, column_type in required_columns.items():

        if column_name not in existing_columns:

            cursor.execute(
                f"""
                ALTER TABLE interviews
                ADD COLUMN {column_name}
                {column_type}
                """
            )

            conn.commit()

    conn.close()


# ==========================================================
# SAVE INTERVIEW
# ==========================================================

def save_interview(
    questions,
    answers,
    evaluation,
    technical_score=0,
    communication_score=0,
    confidence_score=0,
    overall_score=0,
    total_questions=0,
    answered_questions=0,
    skipped_questions=0,
    completion_percentage=0,
    strengths="",
    weaknesses="",
    suggestions=""
):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    interview_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
    INSERT INTO interviews (

        interview_date,

        questions,
        answers,
        evaluation,

        technical_score,
        communication_score,
        confidence_score,
        overall_score,

        total_questions,
        answered_questions,
        skipped_questions,
        completion_percentage,

        strengths,
        weaknesses,
        suggestions

    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        interview_date,

        json.dumps(questions),

        json.dumps(answers),

        clean_evaluation_text(
            evaluation
        ),

        technical_score,
        communication_score,
        confidence_score,
        overall_score,

        total_questions,
        answered_questions,
        skipped_questions,
        completion_percentage,

        strengths,
        weaknesses,
        suggestions
    ))

    conn.commit()
    conn.close()


# ==========================================================
# GET ALL INTERVIEWS
# ==========================================================

def get_all_interviews():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM interviews
    ORDER BY id DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records


# ==========================================================
# GET INTERVIEW BY ID
# ==========================================================

def get_interview_by_id(interview_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM interviews
    WHERE id = ?
    """, (interview_id,))

    record = cursor.fetchone()

    conn.close()

    return record


# ==========================================================
# DELETE INTERVIEW
# ==========================================================

def delete_interview(interview_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM interviews
    WHERE id = ?
    """, (interview_id,))

    conn.commit()
    conn.close()


# ==========================================================
# DELETE ENTIRE HISTORY
# ==========================================================

def clear_database():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM interviews
    """)

    conn.commit()
    conn.close()


# ==========================================================
# TOTAL INTERVIEWS
# ==========================================================

def get_total_interviews():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM interviews
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ==========================================================
# LATEST INTERVIEW
# ==========================================================

def get_latest_interview():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM interviews
    ORDER BY id DESC
    LIMIT 1
    """)

    record = cursor.fetchone()

    conn.close()

    return record


# ==========================================================
# INTERVIEW COUNT
# ==========================================================

def get_interview_count():

    return get_total_interviews()


# ==========================================================
# NORMALIZE RECORD
# ==========================================================

def normalize_interview_record(record):

    normalized = {

        "id": None,

        "date": "",

        "questions": [],

        "answers": {},

        "evaluation": "",

        "technical_score": 0,
        "communication_score": 0,
        "confidence_score": 0,
        "overall_score": 0,

        "total_questions": 0,
        "answered_questions": 0,
        "skipped_questions": 0,
        "completion_percentage": 0,

        "strengths": "",
        "weaknesses": "",
        "suggestions": ""
    }

    if not record:
        return normalized

    try:

        normalized["id"] = record[0]
        normalized["date"] = record[1]

        try:
            normalized["questions"] = json.loads(
                record[2]
            ) if record[2] else []
        except:
            normalized["questions"] = []

        try:
            normalized["answers"] = json.loads(
                record[3]
            ) if record[3] else {}
        except:
            normalized["answers"] = {}

        normalized["evaluation"] = record[4]

        normalized["technical_score"] = record[5]
        normalized["communication_score"] = record[6]
        normalized["confidence_score"] = record[7]
        normalized["overall_score"] = record[8]

        normalized["total_questions"] = record[9]
        normalized["answered_questions"] = record[10]
        normalized["skipped_questions"] = record[11]
        normalized["completion_percentage"] = record[12]

        normalized["strengths"] = record[13]
        normalized["weaknesses"] = record[14]
        normalized["suggestions"] = record[15]

    except Exception:
        pass

    return normalized


# ==========================================================
# NORMALIZED HISTORY
# ==========================================================

def get_normalized_interviews():

    records = get_all_interviews()

    return [
        normalize_interview_record(record)
        for record in records
    ]


# ==========================================================
# ANALYTICS DATA
# ==========================================================

def get_all_scores():

    records = get_all_interviews()

    scores = []

    for record in records:

        normalized = normalize_interview_record(
            record
        )

        scores.append({

            "technical":
                normalized["technical_score"],

            "communication":
                normalized["communication_score"],

            "confidence":
                normalized["confidence_score"],

            "overall":
                normalized["overall_score"],

            "answered":
                normalized["answered_questions"],

            "skipped":
                normalized["skipped_questions"],

            "completion":
                normalized["completion_percentage"]
        })

    return scores