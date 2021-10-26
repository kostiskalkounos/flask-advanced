from models.store import StoreModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

BLANK_ERROR = "'{}' cannot be blank."
ERROR_INSERTING = "An error occurred while creating the store."
NAME_ALREADY_EXISTS = "A Store with name '{}' already exists."
STORE_DELETED = "Store deleted."
STORE_NOT_FOUND = "Store not found."

class Store(Resource):
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
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': STORE_NOT_FOUND}, 404 # this is a tuple


    def post(self, name: str):
        if StoreModel.find_by_name(name):
            return {'message':NAME_ALREADY_EXISTS.format(name)}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'message': ERROR_INSERTING}, 500

        return store.json(), 201

    @jwt_required()
    def delete(self, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': STORE_DELETED}


class StoreList(Resource):
    def get(self):
        # return {'stores': list(map(lambda x: x.json(), StoreModel.find_all()))}
        return {'stores': [store.json() for store in StoreModel.find_all()]}
