from flask_restful import Resource
from flask_jwt import jwt_required

from models.store import StoreModel
from schemas.store import StoreSchema

BLANK_ERROR = "'{}' cannot be blank."
ERROR_INSERTING = "An error occurred while creating the store."
NAME_ALREADY_EXISTS = "A Store with name '{}' already exists."
STORE_DELETED = "Store deleted."
STORE_NOT_FOUND = "Store not found."

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)


class Store(Resource):
    @classmethod
    @jwt_required()
    def get(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store_schema.dump(store)
        return {'message': STORE_NOT_FOUND}, 404 # this is a tuple


    def post(self, name: str):
        if StoreModel.find_by_name(name):
            return {'message':NAME_ALREADY_EXISTS.format(name)}, 400

        store = StoreModel(name=name)

        try:
            store.save_to_db()
        except:
            return {'message': ERROR_INSERTING}, 500

        return store_schema.dump(store), 201

    @classmethod
    @jwt_required()
    def delete(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': STORE_DELETED}


class StoreList(Resource):
    @classmethod
    def get(cls):
        return {'stores': store_list_schema.dump(StoreModel.find_all())}
