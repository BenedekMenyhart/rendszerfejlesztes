from app.blueprints.item.schemas import ItemResponseSchema
from app.blueprints.shipment.schemas import ShipmentResponseSchema
from app.blueprints.supplier.schemas import FewItemResponseSchema
from datetime import datetime, timedelta
from app.extensions import db

from app.models.item import Item

from sqlalchemy import select
from app.models.shipment import Shipment


class SupplierService:

    @staticmethod
    def items_list_few(iid):
        items = db.session.execute(select(Item).filter(Item.id == iid and
                                                       Item.quantity_available < 5)).scalars()
        return True, FewItemResponseSchema().dump(items, many=True)

    @staticmethod
    def shipment_add(iid, sid):
        try:
            items = SupplierService.items_list_few(iid)
            if items:
                shipment = Shipment()
                shipment.expected_at = int((datetime.now() + timedelta(days=1)).timestamp())
                shipment.items.append(items)
                db.session.add(shipment)
                db.session.commit()

                return True, ShipmentResponseSchema().dump({
                    "id": shipment.id,
                    "supplier_id": sid,
                    "items": ItemResponseSchema().dump(items, many=True),
                })

        except Exception as ex:
            return False, "shipment_add() error!"