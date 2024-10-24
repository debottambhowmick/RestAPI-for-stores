from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from models import TagModel, StoreModel
from sqlalchemy.exc import SQLAlchemyError

from schemas import TagSchema, PlainTagSchema

blp = Blueprint("Tags", __name__, description="Operations on tags")

#for creating a new tag in a store or retriving all the tags related to a store
@blp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        return store.tags.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):

        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
            abort(400, message="A tag with the name is already exist hin the store")

        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=f"{str(e)}")
        
        return tag

# Get information about a tag given its unique id, Delete a tag which must not have any item
@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        raise NotImplementedError("The tag delete functionality is not implemented yet")




















# # Link an item of a store with a tag from the same store, Unlike a tag from an item 
# @blp.route("/item/<int:item_id>/tag/<int:tag_id>")
# class TagLink(MethodView):
#     pass
