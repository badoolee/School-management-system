from sqlalchemy import or_
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

from db import db
from schema import StudentSchema
from models import StudentRegister


Studentblp = Blueprint("Students", __name__, description="operation on students")

@Studentblp.route("/Student")
class RegisterStudent(MethodView):
    @jwt_required()
    @Studentblp.arguments(StudentSchema)
    @Studentblp.response(201, StudentSchema)
    def post(self, student_data):
        if StudentRegister.query.filter(
            or_(
                StudentRegister.phone_number == student_data["phone_number"],
                StudentRegister.email == student_data["email"]
            )
            ).first():
                abort(409, message="A student with that phone number or email already exists.")

        student = StudentRegister(**student_data)
            
        try:
            db.session.add(student)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the student info")


        return student

    @jwt_required()
    @Studentblp.response(200, StudentSchema(many=True))
    def get(self):
        return StudentRegister.query.all()


@Studentblp.route("/Student/<int:student_id>")
class StudentList(MethodView):
    @jwt_required()
    @Studentblp.response(200, StudentSchema)
    def get(self, student_id):
        student = StudentRegister.query.get_or_404(student_id)
        return student

    @jwt_required(fresh=True)
    @Studentblp.response(200, StudentSchema)
    def delete(self, student_id):
        student = StudentRegister.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        return {"message": "Student info deleted"}
