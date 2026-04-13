from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grades.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    grade = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def serve_index():
    return send_from_directory(".", "index.html")

@app.route("/style.css")
def serve_css():
    return send_from_directory(".", "style.css")

@app.route("/script.js")
def serve_js():
    return send_from_directory(".", "script.js")

@app.route("/grades", methods=["GET"])
def get_all_grades():
    students = Student.query.all()

    result = {}
    for s in students:
        result[s.name] = s.grade

    return jsonify(result)

@app.route("/grades/<name>", methods=["GET"])
def get_grade(name):
    student = Student.query.filter_by(name=name).first()

    if student:
        return jsonify({student.name: student.grade})
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route("/grades", methods=["POST"])
def add_grade():
    data = request.get_json()

    name = data["name"]
    grade = data["grade"]

    
    existing = Student.query.filter_by(name=name).first()
    if existing:
        return jsonify({"error": "Student already exists"}), 400

    new_student = Student(name=name, grade=grade)
    db.session.add(new_student)
    db.session.commit()

    return jsonify({"message": "Added successfully"})


@app.route("/grades/<name>", methods=["PUT"])
def edit_grade(name):
    student = Student.query.filter_by(name=name).first()

    if not student:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json()
    student.grade = data["grade"]

    db.session.commit()

    return jsonify({"message": "Updated successfully"})


@app.route("/grades/<name>", methods=["DELETE"])
def delete_grade(name):
    student = Student.query.filter_by(name=name).first()

    if not student:
        return jsonify({"error": "Student not found"}), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({"message": "Deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)