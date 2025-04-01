from app.blueprints.storekeeper import bp
from app.blueprints.order.schemas import OrderResponseSchema
from app.blueprints.storekeeper.service import StorekeeperService
from apiflask.fields import String, Integer
from apiflask import HTTPError

@bp.route('/')
def index():
    return 'This is The StoreKeeper Blueprint'


@bp.get("/orders/list/received/<int:rid>")
@bp.output(OrderResponseSchema(many = True))
def storekeeper_orders_list_received(uid):
    success, response = StorekeeperService.storekeeper_orders_list_received(uid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get("/orders/list/processing/<int:rid>")
@bp.output(OrderResponseSchema(many = True))
def storekeeper_orders_list_processing(uid):
    success, response = StorekeeperService.storekeeper_orders_list_processing(uid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.put("/orders/set/processing/<int:oid>")
def storekeeper_orders_processing(oid):
    success, response = StorekeeperService.order_processing(oid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.put("/orders/set/processed/<int:oid>")
def storekeeper_orders_processed(oid):
    success, response = StorekeeperService.order_processed(oid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

