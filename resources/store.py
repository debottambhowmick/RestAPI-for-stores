import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import stores

blp = Blueprint("stores", __name__, description="Operations on stores") 
# this name "stores" can be reffered to later if we wanna craete like between two blueprints
# next argument is the name of the module as dunder name
# the description will go into documentation

# using flask method view we can craete a class whos methods routes to specific endpoints
@blp.route("/store/<string:store_id>") # This decorator made the connection between flask-smorest and flask method view
class Store(MethodView):
    def get(self, store_id):
        try: 
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found!!" )

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message":"Store Deleted !"}
        except KeyError:
            abort(404, message="Store not found.")
    
# similarly for creating a store and getting all the store we need a different class

@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores":list(stores.values())}

    def post(self):
        store_data = request.get_json() 
        # checking for the "name" key in the request
        if "name" not in store_data:
            abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")
        # checking if the store is already present
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message="Store already exists.")

        store_id = uuid.uuid4().hex # long string of numbers as unique identifiers
        store = {**store_data, "id":store_id}
        stores[store_id] = store

        return store, 201