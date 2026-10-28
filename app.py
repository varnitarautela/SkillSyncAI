
from flask import Flask, request, jsonify

from database import create_tables
from student import add_student, get_student, get_all_students
from internship import (
    add_internship,
    get_all_internships,
    delete_internship
)
from recommender import recommend_internships

app = Flask(__name__)

# Create database tables
create_tables()


# HOME PAGE
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to SkillSync AI Backend!",
        "status": "Running successfully"
    })


# STUDENT REGISTRATION
@app.route("/add_student", methods=["POST"])
def register_student():
    data = request.get_json(silent=True) or {}

    name = data.get("name")
    email = data.get("email")
    skills = data.get("skills")

    if not all(
        isinstance(value, str) and value.strip()
        for value in [name, email, skills]
    ):
        return jsonify({
            "error": "Name, email and skills are required"
        }), 400

    try:
        student_id = add_student(
            name.strip(),
            email.strip(),
            skills.strip()
        )

        return jsonify({
            "message": "Student registered successfully!",
            "student_id": student_id
        }), 201

    except Exception as error:
        return jsonify({"error": str(error)}), 400


# VIEW ALL STUDENTS
@app.route("/students", methods=["GET"])
def students():
    return jsonify(get_all_students())


# VIEW ONE STUDENT
@app.route("/student/<int:student_id>", methods=["GET"])
def student_profile(student_id):
    student = get_student(student_id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student)


# ADD INTERNSHIP
@app.route("/add_internship", methods=["POST"])
def register_internship():
    data = request.get_json(silent=True) or {}

    company = data.get("company")
    role = data.get("role")
    skills = data.get("skills_required")
    location = data.get("location", "")

    if not all(
        isinstance(value, str) and value.strip()
        for value in [company, role, skills]
    ):
        return jsonify({
            "error": "Company, role and required skills are required"
        }), 400

    if not isinstance(location, str):
        return jsonify({"error": "Location must be text"}), 400

    internship_id = add_internship(
        company.strip(),
        role.strip(),
        skills.strip(),
        location.strip()
    )

    return jsonify({
        "message": "Internship added successfully!",
        "internship_id": internship_id
    }), 201


# VIEW ALL INTERNSHIPS
@app.route("/internships", methods=["GET"])
def internships():
    return jsonify(get_all_internships())


# DELETE INTERNSHIP
@app.route("/delete_internship/<int:internship_id>",
           methods=["DELETE"])
def remove_internship(internship_id):

    deleted = delete_internship(internship_id)

    if not deleted:
        return jsonify({"error": "Internship not found"}), 404

    return jsonify({
        "message": "Internship deleted successfully!"
    })


# RECOMMEND INTERNSHIPS
@app.route("/recommend/<int:student_id>", methods=["GET"])
def recommendations(student_id):

    result = recommend_internships(student_id)

    if result is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({
        "student_id": student_id,
        "recommendations": result
    })


# RUN APPLICATION
if __name__ == "__main__":
    app.run(debug=True)

