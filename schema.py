from marshmallow import Schema, fields

class AdminSchema(Schema):
    id = fields.Int(dump_only=True)
    surname = fields.Str()
    first_name = fields.Str()
    username = fields.Str()
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class StudentSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    middle_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    age = fields.Int(required=True)
    sex = fields.Str(required=True)
    department = fields.Str(required=True)
    email = fields.Str(required=True)
    phone_number = fields.Int(required=True)
    address = fields.Str(required=True)
    guardian_name = fields.Str(required=True)
    occupation = fields.Str(required=True)
