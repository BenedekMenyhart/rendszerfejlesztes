from app.blueprints.supplier import bp
from app.blueprints.courier.service import CourierService

from app.blueprints.order.schemas import OrderResponseSchema
from app.blueprints.courier.service import CourierService
from apiflask.fields import String, Integer
from apiflask import HTTPError

from app.blueprints.shipment.schemas import ShipmentResponseSchema
from app.blueprints.supplier.schemas import FewItemResponseSchema
from app.blueprints.supplier.service import SupplierService


@bp.route('/')
def supplier_index():
    return 'This is The Supplier Blueprint'


@bp.get("/items/few/<int:iid>")
@bp.output(FewItemResponseSchema(many = True))
def supplier_orders_list_few(iid):
    success, response = SupplierService.items_list_few(iid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get("/items/shipment/<int:iid>/<int:sid>")
@bp.output(ShipmentResponseSchema(many = True))
def shipment_add(iid, sid):
    success, response = SupplierService.shipment_add(iid, sid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


