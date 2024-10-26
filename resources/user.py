from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256

from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity
from blocklist import BLOCKLIST

from db import db
from models import UserModel
from sqlalchemy.exc import SQLAlchemyError

from schemas import UserSchema

blp = Blueprint("Users", __name__, description="Operation on users")


@blp.route("/register")
class UserRegister(MethodView):

    @blp.arguments(UserSchema)
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

        return {"message" : "user added successfully!"},201
    

@blp.route("/login")
class UserLogin(MethodView):

    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password): # if the query that we made in the last line returns none means no user exist with the user name then none and whatever will return none so that way username will be validated and if the hashed version of the password doesnot match then again we cant pass this if condition. so, this way both username password get verified.upon successful verification only we will issue access token
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access token" : access_token, "refresh_token" : refresh_token}
        abort(401, message="Invalid credentials !!")
        
@blp.route("/refresh")
class TokenRefresh(MethodView):

    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt().get('jti')
        BLOCKLIST.add(jti)
        return {"access_token" : new_token}

@blp.route("/logout")
class UserLogout(MethodView):

    @jwt_required() 
    def post(self):
        jti = get_jwt().get("jti")
        BLOCKLIST.add(jti)
        return {"message":"successfully loggedout"}           

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @jwt_required() 
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    @jwt_required() 
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        
        db.session.delete(user)
        db.session.commit()

        return {"message":"user deleted successfully!"}


