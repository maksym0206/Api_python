from marshmallow import Schema, fields
from pydantic import BaseModel, Field

class BookP(BaseModel):
    id: int
    title: str = Field
    author: str


class Book(Schema):
    title = fields.Str(required=True, validate=lambda x: 5 <= len(x))
    author = fields.Str(required=True, validate=lambda x: 5 <= len(x))

