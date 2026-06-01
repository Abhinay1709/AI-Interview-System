import sqlite3

DB_NAME = "interview_data.db"


def create_table():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interviews (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        question TEXT,

        answer TEXT,

        evaluation TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_interview(
    question,
    answer,
    evaluation
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO interviews
        (
            question,
            answer,
            evaluation
        )
        VALUES (?, ?, ?)
        """,
        (
            question,
            answer,
            evaluation
        )
    )

    conn.commit()
    conn.close()


def get_all_interviews():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM interviews"
    )

    data = cursor.fetchall()

    conn.close()

    return data


def delete_interview(record_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM interviews
        WHERE id = ?
        """,
        (record_id,)
    )

    conn.commit()
    conn.close()


def clear_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM interviews"
    )

    conn.commit()
    conn.close()