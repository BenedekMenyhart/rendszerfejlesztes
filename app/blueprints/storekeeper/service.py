from app.extensions import db
from app.blueprints.order.schemas import OrderResponseSchema
from app.models.order import Order, Statuses

from sqlalchemy import select


class StorekeeperService:

    @staticmethod
    def storekeeper_orders_list_received(uid):
        orders = db.session.execute(select(Order).filter(Order.status == Statuses.Received,
                                                         Order.user_id == uid)).scalars()
        return True, OrderResponseSchema().dump(orders, many=True)

    @staticmethod
    def storekeeper_orders_list_processing(uid):
        orders = db.session.execute(select(Order).filter(Order.status == Statuses.Processing,
                                                         Order.user_id == uid)).scalars()
        return True, OrderResponseSchema().dump(orders, many=True)

    @staticmethod
    def order_processing(oid):
        try:
            order = db.session.get(Order, oid)
            if order:
                order.status = Statuses.Processing
                db.session.commit()

        except Exception as ex:
            return False, "order_prepare() error!"
        return True, "OK"

    @staticmethod
    def order_processed(oid):
        try:
            order = db.session.get(Order, oid)
            if order:
                order.status = Statuses.Processed
                db.session.commit()

        except Exception as ex:
            return False, "order_ready() error!"
        return True, "OK"
