from flask import render_template

from app.blueprints import role_required
from app.blueprints.shipment import bp
from apiflask import HTTPError

from app.blueprints.shipment.schemas import ShipmentRequestSchema, ShipmentResponseSchema
from app.blueprints.shipment.service import ShipmentService
from app.extensions import auth


@bp.route('/')
def shipment_index():
    return render_template('shipment.html',  title='Shipment\'s page')


@bp.post('/add')
@bp.doc(tags=["shipment"])
@bp.input(ShipmentRequestSchema, location="json")
@bp.output(ShipmentResponseSchema)
@bp.auth_required(auth)
@role_required(["Courier"])
def shipment_registrate(json_data):
    success, response = ShipmentService.shipment_add(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)