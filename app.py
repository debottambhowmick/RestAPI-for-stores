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
    store_id = uuid.uuid4().hex # long string of numbers as unique identifiers
    store = {**store_data, "id":store_id}
    stores[store_id] = store
    return store, 201

# add item in the store
@app.post("/item")
def create_item():
    item_data = request.get_json()
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