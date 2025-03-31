from app.blueprints.courier import bp

from app.blueprints.order.schemas import OrderResponseSchema
from app.blueprints.courier.service import CourierService
from apiflask.fields import String, Integer
from apiflask import HTTPError

@bp.route('/')
def index():
    return 'This is The Courier Blueprint'


@bp.get("/orders/list/ready/<int:rid>")
@bp.output(OrderResponseSchema(many = True))
def courier_orders_list_ready(rid):
    success, response = CourierService.orders_list_ready(rid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get("/orders/list/delivery/<int:rid>")
@bp.output(OrderResponseSchema(many = True))
def courier_orders_list_delivery(rid):
    success, response = CourierService.orders_list_delivery(rid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.put("/orders/set/delivery/<int:oid>")
def courier_orders_delivery(oid):
    success, response = CourierService.order_delivery(oid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.put("/orders/set/delivered/<int:oid>")
def courier_orders_delivered(oid):
    success, response = CourierService.order_delivered(oid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.put("/orders/set/canceled/<int:oid>")
@bp.input({'reason': String()}, location='query', )
def chef_set_delivered(oid, query_data):
    success, response = CourierService.order_canceled(oid, query_data["reason"])
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)
