from flask import Flask, request
from db import items, stores
from flask_smorest import abort
import uuid
app = Flask(__name__)


# getting all stores information
@app.get("/store")
def get_stores():
    return {"stores":list(stores.values())}

# craete a store
@app.post("/store")
def create_store():
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

# add item in the store
@app.post("/item")
def create_item():
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

#get all items
app.get("/item")
def get_all_items():
    return {items:list(items.values())}

# getting an individual store           
@app.get("/store/<string:store_id>")
def  get_store(store_id):
        try: 
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found!!" )

# get item of a store
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found!!" )