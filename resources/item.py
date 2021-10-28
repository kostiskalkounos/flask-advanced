from flask import request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask_restful import Resource
from models.item import ItemModel
from schemas.item import ItemSchema

ADMIN_PRIVILEGES_REQUIRED = "Admin privileges required."
ERROR_INSERTING = 'An error occurred inserting the item.'
ITEM_DELETED = "Item deleted."
ITEM_NOT_FOUND = "Item not found."
MORE_DATA_AVAILABLE = "More data available if you log in."
NAME_ALREADY_EXISTS = "An Item with name '{}' already exists."

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)

class Item(Resource):
    @classmethod
    @jwt_required()
    def get(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item), 200
        return {'message': ITEM_NOT_FOUND}, 404


    @classmethod
    @jwt_required(fresh=True)
    def post(cls, name: str): # /item/chair
        if ItemModel.find_by_name(name):
            return {'message': NAME_ALREADY_EXISTS.format(name)}, 400

        user_json = request.get_json() # price, store_id
        user_json["name"] = name

        item = item_schema.load(user_json)

        try:
            item.save_to_db()
        except:
            return {'message': ERROR_INSERTING}, 500

        return item_schema.dump(item), 201

    @classmethod
    @jwt_required()
    def delete(cls, name: str):
        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': ADMIN_PRIVILEGES_REQUIRED}

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': ITEM_DELETED}, 200

        return {'message': ITEM_NOT_FOUND}, 404

    @classmethod
    @jwt_required()
    def put(cls, name: str):
        item_json = request.get_json()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = item_json['price']
        else:
            item_json["name"] = name
            item = item_schema.load(item_json)

        item.save_to_db()

        return item_schema.dump(item)


class ItemList(Resource):
    @classmethod
    @jwt_required(optional=True)
    def get(cls):
        user_id = get_jwt_identity()
        items = item_list_schema.dump(ItemModel.find_all())
        if user_id:
            return {'items': items}, 200
        return {
            'items': [item['name'] for item in items],
            'message': MORE_DATA_AVAILABLE
        }, 200
