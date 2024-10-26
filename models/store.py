from db import db

class StoreModel(db.Model): # This creates a mapping between each row in the table to a python class
    __tablename__ = "stores" # name of teh table

    id = db.Column(db.Integer, primary_key=True) # integer datatype and primary key
    name = db.Column(db.String(80), unique=True, nullable=False) # string datatype, unique, can not be null
    
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete")
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic", cascade="all, delete")
    
    