from app.extensions import db
from app.blueprints.order.schemas import OrderItemSchema, OrderResponseSchema, OrderRequestSchema, \
    FeedbackResponseSchema

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



    @staticmethod
    def feedback_add(order_id):
        try:

            order = db.session.get(Order, order_id)
            if not order:
                return False, f"Order with id {order_id} not found."


            feedback = input("Enter feedback: ")
            order.feedback = feedback
            order.status = Statuses.ReceptionConfirmed

            db.session.commit()

        except Exception as ex:
            return False, f"feedback_add() error: {str(ex)}"

        return True, FeedbackResponseSchema().dump({
            "id": order.id,
            "order": [OrderResponseSchema().dump(order)],
            "feedback": order.feedback
        })

