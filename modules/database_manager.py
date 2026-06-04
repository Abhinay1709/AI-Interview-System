import sqlite3
import json
from datetime import datetime

DB_NAME = "interview_data.db"


def create_table():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    # Create table if it doesn't exist at all
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interviews (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        interview_date TEXT,

        questions TEXT,

        answers TEXT,

        evaluation TEXT
    )
    """)

    conn.commit()

    # FIX: Migrate existing DB that was created without interview_date column.
    # ALTER TABLE ADD COLUMN is safe to call — we catch the error if
    # the column already exists and continue normally.
    existing_columns = [
        row[1]
        for row in cursor.execute(
            "PRAGMA table_info(interviews)"
        ).fetchall()
    ]

    if "interview_date" not in existing_columns:

        cursor.execute(
            """
            ALTER TABLE interviews
            ADD COLUMN interview_date TEXT
            """
        )

        conn.commit()

    if "questions" not in existing_columns:

        cursor.execute(
            """
            ALTER TABLE interviews
            ADD COLUMN questions TEXT
            """
        )

        conn.commit()

    if "answers" not in existing_columns:

        cursor.execute(
            """
            ALTER TABLE interviews
            ADD COLUMN answers TEXT
            """
        )

        conn.commit()

    if "evaluation" not in existing_columns:

        cursor.execute(
            """
            ALTER TABLE interviews
            ADD COLUMN evaluation TEXT
            """
        )

        conn.commit()

    conn.close()


def save_interview(
    questions,
    answers,
    evaluation
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    interview_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    questions_json = json.dumps(
        questions
    )

    answers_json = json.dumps(
        answers
    )

    cursor.execute(
        """
        INSERT INTO interviews
        (
            interview_date,
            questions,
            answers,
            evaluation
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            interview_date,
            questions_json,
            answers_json,
            evaluation
        )
    )

    conn.commit()
    conn.close()


def get_all_interviews():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM interviews
        ORDER BY id ASC
        """
    )

    data = cursor.fetchall()

    conn.close()

    return data


def get_interview_by_id(
    interview_id
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM interviews
        WHERE id = ?
        """,
        (interview_id,)
    )

    record = cursor.fetchone()

    conn.close()

    return record


def delete_interview(
    interview_id
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM interviews
        WHERE id = ?
        """,
        (interview_id,)
    )

    conn.commit()
    conn.close()


def clear_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM interviews
        """
    )

    conn.commit()
    conn.close()


def get_total_interviews():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM interviews
        """
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total