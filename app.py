from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_uploads import configure_uploads, patch_request_class
from marshmallow import ValidationError
from dotenv import load_dotenv

from blocklist import BLOCKLIST
from db import db
from ma import ma
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import TokenRefresh, User, UserLogin, UserLogout, UserRegister
from resources.image import ImageUpload, Image, AvatarUpload, Avatar
from libs.image_helper import IMAGE_SET

app = Flask(__name__)
load_dotenv(".env", verbose=True)
app.config.from_object("default_config")
app.config.envvar("APPLICATION_SETTINGS")
patch_request_class(app, 10 * 1024 * 1024) # 10MB max size upload
configure_uploads(app, IMAGE_SET)
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.errorhandler(ValidationError)
def handle_marshmallow__validation(err):
    return jsonify(err.messages), 400

jwt = JWTManager(app)

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(decrypted_token):
    return decrypted_token['jti'] in BLOCKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback():
    return jsonify({
        'description': 'Signature verification failed',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback():
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401

api.add_resource(Avatar, '/avatar/<int:user_id>')
api.add_resource(AvatarUpload, '/upload/avatar')
api.add_resource(Confirmation, '/user_confirmation/<string:confirmation_id>')
api.add_resource(ConfirmationByUser, '/confirmation/user/<int:user_id>')
api.add_resource(Image, '/image/<string:filename>')
api.add_resource(ImageUpload, '/upload/image')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000)
