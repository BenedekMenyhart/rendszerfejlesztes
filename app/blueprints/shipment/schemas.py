from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List

class ShipmentItemSchema(Schema):
    item_id = fields.Integer()
    quantity = fields.Integer()

class ShipmentRequestSchema(Schema):
    supplier_id = fields.Integer()
    items = fields.Nested(ShipmentItemSchema(many=True))


class ShipmentResponseSchema(Schema):
    id = fields.Integer()
    supplier_id = fields.Integer()
    items = fields.Nested(ShipmentItemSchema(many=True))



