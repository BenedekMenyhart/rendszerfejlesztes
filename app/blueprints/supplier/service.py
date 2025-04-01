from sqlalchemy.testing.suite.test_reflection import users

from app.blueprints import supplier
from app.blueprints.item.schemas import ItemResponseSchema
from app.blueprints.shipment.schemas import ShipmentResponseSchema
from app.blueprints.supplier.schemas import FewItemSchema, FewItemResponseSchema
from datetime import datetime, timedelta
from app.extensions import db
from app.blueprints.order.schemas import OrderResponseSchema
from app.models.user import User
from app.models.item import Item
from app.models.order import Order, Statuses

from sqlalchemy import select, and_

from app.models.shipment import Shipment


class SupplierService:

    @staticmethod
    def items_list_few(iid):
        items = db.session.execute(select(Item).filter(Item.id == iid and
                                                       Item.quantity_available < 5)).scalars()
        return True, FewItemResponseSchema().dump(items, many=True)

    @staticmethod
    def shipment_add(iid):
        try:
            items = SupplierService.items_list_few(iid)
            if items:
                shipment = Shipment()
                shipment.expected_at = int((datetime.now() + timedelta(days=1)).timestamp())
                shipment.items.append(items)
                db.session.add(shipment)
                db.session.commit()

        except Exception as ex:
            return False, "shipment_add() error!"
        return True, ShipmentResponseSchema().dump({
            "id": shipment.id,
            "supplier_id": users.get_current_user().id,
            "items": ItemResponseSchema().dump(items, many=True),
        })