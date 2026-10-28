
from database import connect_db


def add_internship(company, role, skills_required, location):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO internships
        (company, role, skills_required, location)
        VALUES (?, ?, ?, ?)
        """,
        (company, role, skills_required, location)
    )

    internship_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return internship_id


def get_all_internships():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM internships")

    internships = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return internships


def delete_internship(internship_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM internships WHERE id = ?",
        (internship_id,)
    )

    deleted = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return deleted
