from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List
from apiflask.validators import Length, OneOf, Email
from app.blueprints.user.schemas import AddressSchema


class OrderItemSchema(Schema):
    item_id = fields.Integer()
    quantity = fields.Integer()


class OrderRequestSchema(Schema):
    user_id = fields.Integer()
    address_id = fields.Integer()
    items = fields.Nested(OrderItemSchema(many=True))


class OrderResponseSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    address = fields.Nested(AddressSchema)
    items = fields.Nested(OrderItemSchema(many=True))

