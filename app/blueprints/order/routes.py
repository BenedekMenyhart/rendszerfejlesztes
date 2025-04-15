from app.blueprints import role_required
from app.blueprints.order import bp
from app.blueprints.order.schemas import OrderItemSchema, OrderRequestSchema, OrderResponseSchema, \
    FeedbackRequestSchema, FeedbackResponseSchema
from app.blueprints.order.service import OrderService
from apiflask.fields import String, Integer
from apiflask import HTTPError

from app.extensions import auth


@bp.route('/')
def order_index():
    return 'This is The Order Blueprint'


@bp.post('/add')
@bp.doc(tags=["order"])
@bp.auth_required(auth)
@role_required(["User"])
@bp.input(OrderRequestSchema, location="json")
@bp.output(OrderResponseSchema)
def order_registrate(json_data):
    success, response = OrderService.order_add(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.post('/feedback')
@bp.doc(tags=["order"])
@bp.input(FeedbackRequestSchema, location="json")
@bp.output(FeedbackResponseSchema)
@bp.auth_required(auth)
@role_required(["User"])
def feedback_registrate(json_data):
    success, response = OrderService.feedback_add(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)