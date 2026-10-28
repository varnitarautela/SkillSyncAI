
from database import connect_db


def add_student(name, email, skills):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO students (name, email, skills)
        VALUES (?, ?, ?)
        """,
        (name, email, skills)
    )

    student_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return student_id


def get_student(student_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()
    conn.close()

    return dict(student) if student else None


def get_all_students():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    students = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return students
