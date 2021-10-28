from marshmallow import Schema, fields


class UserSchema(Schema):
    class Meta:
        load_only = ("password",) # it's a tuple
        dump_only = ("id",) # not required in this scenario

    id = fields.Int()
    username = fields.Str(required=True)
    password = fields.Str(required=True)
