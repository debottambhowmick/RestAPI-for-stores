from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from models import TagModel, StoreModel, ItemModel
from sqlalchemy.exc import SQLAlchemyError

from schemas import TagSchema, PlainTagSchema, TagAndItemSchema

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

    # some alternative responses added to tackle different scenarios
    @blp.response (202, description="Delete a tag if no item is tagged", example={"message":"Tag Deleted."})
    @blp.alt_response(404, description="Tag Not Found.")
    @blp.alt_response(400, description="Returned if the tag is linked to one or more items. In this case, the tag is not deleted.")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        
        abort(400, message="Tag can't be deleted. make sure tag is not linked to any item, then try again.")




# Link an item of a store with a tag from the same store, Unlike a tag from an item 
@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if item.store_id != tag.store_id:
            abort(400, message="Make sure item and tag belong to the same store before linking.")

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="AN error occured while linking the tag")

        return tag
    
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="AN error occured while unlinking the tag")

        return {"message" : f"Item:{item} unlinked from tag:{tag} "}
    


    


