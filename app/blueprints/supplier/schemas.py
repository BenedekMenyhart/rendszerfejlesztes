from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List

class FewItemSchema(Schema):
    item_id = fields.Integer()
    quantity = fields.Integer()

class FewItemRequestSchema(Schema):
    supplier_id = fields.Integer()
    items = fields.Nested(FewItemSchema(many=True))


class FewItemResponseSchema(Schema):
    id = fields.Integer()
    supplier_id = fields.Integer()
    items = fields.Nested(FewItemSchema(many=True))






