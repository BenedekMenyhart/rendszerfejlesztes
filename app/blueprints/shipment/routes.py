from app.blueprints.order import bp
from apiflask.fields import String, Integer
from apiflask import HTTPError

from app.blueprints.shipment.schemas import ShipmentRequestSchema, ShipmentResponseSchema
from app.blueprints.shipment.service import ShipmentService


@bp.route('/')
def shipment_index():
    return 'This is The Shipment Blueprint'


@bp.post('/add')
@bp.doc(tags=["shipment"])
@bp.input(ShipmentRequestSchema, location="json")
@bp.output(ShipmentResponseSchema)
def shipment_registrate(json_data):
    success, response = ShipmentService.shipment_add(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)