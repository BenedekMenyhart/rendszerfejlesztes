from app.blueprints.storekeeper import bp
from app.blueprints.order.schemas import OrderResponseSchema
from app.blueprints.storekeeper.service import StorekeeperService
from apiflask.fields import String, Integer
from apiflask import HTTPError

@bp.route('/')
def index():
    return 'This is The StoreKeeper Blueprint'


@bp.get("/orders/list/created/<int:rid>")
@bp.output(OrderResponseSchema(many = True))
def storekeeper_orders_list_created(rid):
    success, response = StorekeeperService.storekeeper_orders_list_created(rid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get("/orders/list/prepare/<int:rid>")
@bp.output(OrderResponseSchema(many = True))
def storekeeper_orders_list_prepare(rid):
    success, response = StorekeeperService.storekeeper_orders_list_prepare(rid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.put("/orders/set/prepare/<int:oid>")
def storekeeper_orders_prepare(oid):
    success, response = StorekeeperService.order_prepare(oid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.put("/orders/set/ready/<int:oid>")
def storekeeper_orders_ready(oid):
    success, response = StorekeeperService.order_ready(oid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

