from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError , IntegrityError

from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores") 


# using flask MethodView we can craete a class whos methods routes to specific endpoints
@blp.route("/store/<string:store_id>") # This decorator made the connection between flask-smorest and flask method view
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store= StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
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