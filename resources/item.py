from models.item import ItemModel
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

ADMIN_PRIVILEGES_REQUIRED = "Admin privileges required."
BLANK_ERROR = "'{}' cannot be blank."
ERROR_INSERTING = 'An error occurred inserting the item.'
ITEM_DELETED = "Item deleted."
ITEM_NOT_FOUND = "Item not found."
MORE_DATA_AVAILABLE = "More data available if you log in."
NAME_ALREADY_EXISTS = "An Item with name '{}' already exists."

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                         type=float,
                         required=True,
                         help=BLANK_ERROR.format("price")
    )

    parser.add_argument('store_id',
                         type=int,
                         required=True,
                         help=BLANK_ERROR.format("store_id")
    )

    @jwt_required()
    def get(self, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': ITEM_NOT_FOUND}, 404


    @jwt_required(fresh=True)
    def post(self, name: str):
        if ItemModel.find_by_name(name):
            return {'message': NAME_ALREADY_EXISTS.format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': ERROR_INSERTING}, 500

        return item.json(), 201

    @jwt_required()
    def delete(self, name: str):
        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': ADMIN_PRIVILEGES_REQUIRED}

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': ITEM_DELETED}, 200

        return {'message': ITEM_NOT_FOUND}, 404

    @jwt_required()
    def put(self, name: str):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200
        return {
            'items': [item['name'] for item in items],
            'message': MORE_DATA_AVAILABLE
        }, 200
