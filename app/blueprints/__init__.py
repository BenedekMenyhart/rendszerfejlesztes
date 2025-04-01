from apiflask import APIBlueprint

bp = APIBlueprint('main', __name__, tag='Main')

from app.blueprints import bp

@bp.route('/')
def index():
    return 'his is The Main Blueprint'

#register blueprints here
from app.blueprints.user import bp as bp_user
bp.register_blueprint(bp_user, url_prefix='/user')

from app.blueprints.item import bp as bp_item
bp.register_blueprint(bp_item, url_prefix='/item')

from app.blueprints.order import bp as bp_order
bp.register_blueprint(bp_order, url_prefix='/order')

from app.blueprints.storekeeper import bp as bp_storekeeper
bp.register_blueprint(bp_storekeeper, url_prefix='/storekeeper')

from app.blueprints.courier import bp as bp_courier
bp.register_blueprint(bp_courier, url_prefix='/courier')

from app.blueprints.shipment import bp as bp_shipment
bp.register_blueprint(bp_shipment, url_prefix='/shipment')

from app.models import *