from sqlalchemy import or_
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

from db import db
from models import AdminRegistration, TokenBlocklist
from schema import AdminSchema

Adminblp = Blueprint("Admin", __name__, description="operation on admin.")

@Adminblp.route("/Register")
class AdminRegister(MethodView):
    @Adminblp.arguments(AdminSchema)
    def post(self, admin_data):
        if AdminRegistration.query.filter(
            or_(
                AdminRegistration.username == admin_data["username"],
                AdminRegistration.email == admin_data["email"]
            )
            ).first():
                abort(409, message="A user with that username or email already exists.")

        admin = AdminRegistration(
                surname=admin_data["surname"],
                first_name=admin_data["first_name"],
                username=admin_data["username"],
                email=admin_data["email"],
                password=pbkdf2_sha256.hash(admin_data["password"])
            )

        db.session.add(admin)
        db.session.commit()

        return {"message": "User created successfully"}, 201

@Adminblp.route("/Login")
class AdminLogin(MethodView):
    @Adminblp.arguments(AdminSchema)
    def post(self, admin_data):
        admin = AdminRegistration.query.filter(
            AdminRegistration.email == admin_data["email"]
            ).first()

        if admin and pbkdf2_sha256.verify(admin_data["password"], admin.password):
            access_token = create_access_token(identity=admin.id, fresh=True)
            refresh_token = create_refresh_token(identity=admin.id)
            return {"access_token": access_token, "refresh_token": refresh_token}

        abort(401, message="Invalid credentials")


@Adminblp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        db.session.add(TokenBlocklist(jti=jti))
        db.session.commit()
        return {"access_token": new_token}


@Adminblp.route("/Logout")
class AdminLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        db.session.add(TokenBlocklist(jti=jti))
        db.session.commit()
        return {"message": "Logout Successfully"}
        
