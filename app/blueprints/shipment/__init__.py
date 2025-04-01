from apiflask import APIBlueprint

bp = APIBlueprint('shipment', __name__, tag="shipment")

from app.blueprints.shipment import routes