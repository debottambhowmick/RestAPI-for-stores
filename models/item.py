from db import db

class ItemModel(db.Model): # This creates a mapping between each row in the table to a python class
    __tablename__ = "items" # name of teh table

    id = db.Column(db.Integer, primary_key=True) # integer datatype and primary key
    name = db.Column(db.String(80), unique=True, nullable=False) # string datatype, unique, can not be null
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)#float, not unique, can not be null
    store_id = db.Column(db.Integer,db.ForeignKey("stores.id"), unique=False, nullable=False)#Integer , not unique, can not be null
    stores = db.relationship("StoreModel", back_populates="items", lazy="dynamic") 



