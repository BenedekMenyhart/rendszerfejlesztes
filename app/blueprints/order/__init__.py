from apiflask import APIBlueprint

bp = APIBlueprint('order', __name__, tag="order")

from app.blueprints.order import routes
