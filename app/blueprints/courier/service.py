from app.extensions import db

from app.models.order import Order, Statuses

from sqlalchemy import select


class CourierService:



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