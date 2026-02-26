from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///grades.db"

db = SQLAlchemy(app)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id" : self.id,
            "subject" : self.subject,
            "semester" : self.semester,
            "grade" : self.grade
        }
    
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({"message": "Welcome to grades API"})

@app.route("/subject/<string:subject_name>", methods=["GET"])
def get_subject(subject_name):
    subject = Subject.query.filter_by(subject=subject_name).first()
    if subject:
        return jsonify(subject.to_dict())
    else:
        return jsonify({"error" : "Subject not fount"}), 404

@app.route("/subject/add", methods=["POST"])
def add_subject():
    data = request.get_json()

    new_subject = Subject(subject=data["subject"],
                          semester=data["semester"],
                          grade=data["grade"])
    
    db.session.add(new_subject)
    db.session.commit()

    return jsonify(new_subject.to_dict()), 201

@app.route("/subject/average", methods=["GET"])
def get_global_average():
    subject_objects = Subject.query.all()

    data = [s.to_dict() for s in subject_objects]

    sum = 0
    count = 0

    for item in data:
        sum += item["grade"]
        count += 1

    if count > 0:
        global_average = sum / count
    else:
        global_average = 0
    
    return jsonify({"global_average" : round(global_average, 2)})

@app.route("/subject/<string:subject_name>", methods=["PUT"])
def put_subject(subject_name):
    updated_subject = request.get_json()
    subject = Subject.query.filter_by(subject=subject_name).first()
    if subject:
        subject.subject = updated_subject.get("subject", subject.subject)
        subject.semester = updated_subject.get("semester", subject.semester)
        subject.grade = updated_subject.get("grade", subject.grade)

        db.session.commit()
        return jsonify(subject.to_dict())
    else:
        return jsonify({"error" : "Subject not fount"}), 404
    
@app.route("/subject/<string:subject_name>", methods=["DELETE"])
def delete_subject(subject_name):
    subject = Subject.query.filter_by(subject=subject_name).first()
    if subject:
        db.session.delete(subject)

        db.session.commit()
        return jsonify({"message" : "subject deleted"})
    else:
        return jsonify({"error" : "Subject not fount"}), 404
    
@app.route("/get_all", methods=["GET"])
def get_all():
    subjects = Subject.query.all()
    return jsonify([subject.to_dict() for subject in subjects])

@app.route("/get_semester/<int:id_semester>", methods=["GET"])
def get_by_semester(id_semester):
    subjects = Subject.query.filter_by(semester=id_semester).all()
    
    return jsonify([subject.to_dict() for subject in subjects])


if __name__ == "__main__":
    app.run(debug=True)