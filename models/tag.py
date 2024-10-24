from db import db

class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False) 
    # intentinally making the unique false because if we keep it True then no two tags would have same names accross different stores. which contradicts real world business logic. We want no two tag would have same name in a particular store and we can implement that while creating a new tag using manual logic , sql alchemy by defualt doesnot provide any constaint to do that
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)

    store = db.relationship('StoreModel', back_populates="tags")