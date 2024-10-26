from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError , IntegrityError

from flask_jwt_extended import jwt_required, get_jwt

from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores") 


# using flask MethodView we can craete a class whos methods routes to specific endpoints
@blp.route("/store/<int:store_id>") # This decorator made the connection between flask-smorest and flask method view
class Store(MethodView):

    @jwt_required()
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store= StoreModel.query.get_or_404(store_id)
        return store

    @jwt_required()
    def delete(self, store_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilage required !")
        store= StoreModel.query.get_or_404(store_id) 
        db.session.delete(store)
        db.session.commit()
        return {"message" : "Store Deleted !!"}
    
    
# similarly for creating a store and getting all the store we need a different class

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with the name already Exist" )
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the item")

        return store