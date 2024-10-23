import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items
from db import stores

blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found!!" )

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found!!" )

    def put(self, item_id):
        item_data = request.get_json()
        if "price" not in item_data or "name" not in item_data:
            abort(400, message="Bad request. Ensure 'price' and 'name' are included in the JSON payload.")
        try:
            item = items[item_id]
            item["name"] = item_data["name"]
            item["price"] = item_data["price"]
            ## item |= item_data  # short cut to update dictionary
            return item
        except KeyError:
            abort(404, "Item not Found.")

@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items":list(items.values())}
    
    def post(self):
        item_data = request.get_json()
        #checking if all the expected keys are present or not
        if ("price" not in item_data or "store_id" not in item_data or "name" not in item_data):
            abort (400, message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.")
        # checking if the item is already present
        for item in items.values():
            if item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]:
                abort(400, "Item already Exists.")
        # checking if the store id passed by client is valid
        if item_data["store_id"] not in stores:
            abort(404, message="Store not found!!" )
        
        item_id = uuid.uuid4().hex
        item = {**item_data, "id" : item_id}
        items[item_id] = item

        return item, 201