from ma import ma
from models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ("password",) # it's a tuple
        dump_only = ("id", "activated") # not required in this scenario
