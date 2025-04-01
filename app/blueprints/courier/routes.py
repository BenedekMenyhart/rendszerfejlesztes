from app.blueprints.courier import bp
from app.blueprints.courier.service import CourierService

from app.blueprints.order.schemas import OrderResponseSchema
from app.blueprints.courier.service import CourierService
from apiflask.fields import String, Integer
from apiflask import HTTPError

@bp.route('/')
def index():
    return 'This is The Courier Blueprint'


@bp.get("/orders/list/processed/<int:rid>")
@bp.output(OrderResponseSchema(many = True))
def courier_orders_list_processed(rid):
    success, response = CourierService.orders_list_processed(rid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get("/orders/list/assigned_to_courier/<int:rid>")
@bp.output(OrderResponseSchema(many = True))
def courier_orders_list_assigned_to_courier(rid):
    success, response = CourierService.orders_list_assigned_to_courier(rid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.put("/orders/set/delivery_started/<int:oid>")
def courier_orders_delivery_started(oid):
    success, response = CourierService.order_delivery_started(oid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.put("/orders/set/delivered/<int:oid>")
def courier_orders_delivered(oid):
    success, response = CourierService.order_delivered(oid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)
