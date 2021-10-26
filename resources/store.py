from models.store import StoreModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                         type=float,
                         required=True,
                         help='This field cannot be left blank.'
    )

    parser.add_argument('store_id',
                         type=int,
                         required=True,
                         help='Every item needs a store id.'
    )

    @jwt_required()
    def get(self, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404 # this is a tuple


    def post(self, name: str):
        if StoreModel.find_by_name(name):
            return {'message': "A Store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred while creating the store.'}, 500

        return store.json(), 201

    @jwt_required()
    def delete(self, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):
    def get(self):
        # return {'stores': list(map(lambda x: x.json(), StoreModel.find_all()))}
        return {'stores': [store.json() for store in StoreModel.find_all()]}
