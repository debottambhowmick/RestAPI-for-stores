from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256

from db import db
from models import UserModel
from sqlalchemy.exc import SQLAlchemyError

from schemas import UserSchema

blp = Blueprint("Users", __name__, description="Operation on users")


@blp.route("/register")
class UserRegister(MethodView):

    @blp.arguments(UserSchema)
    @blp.response(201,UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user Id with that username already exists")
        user = UserModel(
            username = user_data["username"],
            password = pbkdf2_sha256.hash(user_data["password"])
        )
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while registering the user")

        return {"message":"user added successfully!"}
    
    
@blp.route("/user/<int:user_id>")
class User(MethodView):

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        
        db.session.delete(user)
        db.session.commit()

        return {"message":"user deleted successfully!"}

