
from database import connect_db


def recommend_internships(student_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Get student details
    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if student is None:
        conn.close()
        return None

    # Convert student skills into a set
    student_skills = {
        skill.strip().lower()
        for skill in student["skills"].split(",")
        if skill.strip()
    }

    # Get all internships
    cursor.execute("SELECT * FROM internships")
    internships = cursor.fetchall()

    recommendations = []

    for internship in internships:

        required_skills = {
            skill.strip().lower()
            for skill in internship["skills_required"].split(",")
            if skill.strip()
        }

        if not required_skills:
            continue

        # Find matching skills
        matched_skills = student_skills.intersection(
            required_skills
        )

        # Calculate match percentage
        percentage = (
            len(matched_skills) / len(required_skills)
        ) * 100

        recommendations.append({
            "internship_id": internship["id"],
            "company": internship["company"],
            "role": internship["role"],
            "location": internship["location"],
            "matched_skills": sorted(matched_skills),
            "missing_skills": sorted(
                required_skills - student_skills
            ),
            "match_percentage": round(percentage, 2)
        })

    conn.close()

    # Show highest matching internships first
    recommendations.sort(
        key=lambda x: x["match_percentage"],
        reverse=True
    )

    return recommendations
