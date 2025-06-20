from app.extensions import db
from app.models.order import Order, Statuses

from sqlalchemy import select


class StorekeeperService:

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
