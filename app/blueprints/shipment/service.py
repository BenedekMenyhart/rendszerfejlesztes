from app.blueprints.shipment.schemas import ShipmentResponseSchema
from app.extensions import db
from app.models import shipment

from app.models.shipmentitem import ShipmentItem


class ShipmentService:

    @staticmethod
    def shipment_add(request):
        try:
            request["items"] = [ShipmentItem(**item) for item in request["items"]]
            db.session.add(shipment)
            db.session.commit()
        except Exception as ex:
            return False, "shipment_add() error!"
        return True, ShipmentResponseSchema().dump(shipment)

