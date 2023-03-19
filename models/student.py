from db import db

class StudentRegister(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    middle_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(20), nullable=False)
    department = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.Integer, unique=True, nullable=False)
    address = db.Column(db.String(256), nullable=False)
    guardian_name = db.Column(db.String(80), nullable=False)
    occupation = db.Column(db.String(80), nullable=False)
