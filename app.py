import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db
import models

from blocklist import BLOCKLIST

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

def create_app(db_url=None):
    app = Flask(__name__)

    load_dotenv()

    app. config["PROPAGATE_EXCEPTIONS"] = True
    app.config[ "API_TITLE"] = "Stores REST API"
    app. config["API_VERSION"] = "v1"
    app. config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "29065815158482322679658826655823704703"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader # whenever we recieve a jwt, this function runs and checks wheather the toekn is in the blocklist if this function return true , then the request is terminated and user will get an error , "token is revoked"
    def check_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    # upon the error for added access token to block list the user will get error message and we can customize the message from here
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description" : "The token has revoked.", "error" : "token revoked"}
            ),
            401
        )
    
    @jwt.needs_fresh_token_loader
    def needs_fresh_token(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token is not fresh", "error": "fresh token required, login again!!"}
                ),
                401
        )   
    
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1: # this is not efficient to add a user id for admin rather we can check the database to find that
            return {"is_admin" : True}
        return {"is_admin" : False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401
        )
    
    # with app.app_context():
    #     db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app