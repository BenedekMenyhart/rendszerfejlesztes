from app.extensions import db
from app.blueprints.order.schemas import OrderResponseSchema
from app.models.order import Order, Statuses

from sqlalchemy import select


class CourierService:

    @staticmethod
    def orders_list_processed(rid):
        orders = db.session.execute(select(Order).filter(Order.status == Statuses.Processed)).scalars()
        return True, OrderResponseSchema().dump(orders, many=True)

    @staticmethod
    def orders_list_assigned_to_courier(rid):
        orders = db.session.execute(select(Order).filter(Order.status == Statuses.AssignedToCourier)).scalars()
        return True, OrderResponseSchema().dump(orders, many=True)

    @staticmethod
    def order_delivery_started(oid):
        try:
            order = db.session.get(Order, oid)
            if order:
                order.status = Statuses.DeliveryStarted
                db.session.commit()

        except Exception as ex:
            return False, "order_delivery_started() error!"
        return True, "OK"

    @staticmethod
    def order_delivered(oid):
        try:
            order = db.session.get(Order, oid)
            if order:
                order.status = Statuses.Delivered
                db.session.commit()

        except Exception as ex:
            return False, "order_delivered() error!"
        return True, "OK"