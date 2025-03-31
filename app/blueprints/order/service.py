from app.extensions import db
from app.blueprints.order.schemas import OrderItemSchema, OrderResponseSchema, OrderRequestSchema

from app.models.item import Item
from app.models.orderitem import OrderItem
from app.models.order import Order, Statuses

from sqlalchemy import select, and_


class OrderService:

    @staticmethod
    def order_add(request):
        try:
            request["items"] = [OrderItem(**item) for item in request["items"]]
            order = Order(**request)
            order.status = Statuses.Received
            db.session.add(order)
            db.session.commit()
        except Exception as ex:
            return False, "order_add() error!"
        return True, OrderResponseSchema().dump(order)
