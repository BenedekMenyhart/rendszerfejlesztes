from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List
from apiflask.validators import Length, OneOf, Email

from app.models.item import Item


class ItemRequestSchema(Schema):
    name = fields.String()
    description = fields.String()
    price = fields.Float()


class ItemResponseSchema(Schema):
    name = fields.String()
    description = fields.String()
    price = fields.Float()


class ItemListSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    price = fields.Float()