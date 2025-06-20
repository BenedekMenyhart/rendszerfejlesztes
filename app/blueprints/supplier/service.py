
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

