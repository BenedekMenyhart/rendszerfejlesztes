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

from app.models import *