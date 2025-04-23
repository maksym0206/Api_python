from marshmallow import Schema, fields

class Book(Schema):
    title = fields.Str(required=True, validate=lambda x: 5 <= len(x))
    author = fields.Str(required=True, validate=lambda x: 3 <= len(x))

    