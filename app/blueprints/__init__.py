#from flask import Blueprint
from apiflask import APIBlueprint
bp = APIBlueprint('main', __name__, tag="default")
from functools import wraps
from app.extensions import auth
from flask import current_app
from authlib.jose import jwt
from datetime import datetime
from apiflask import HTTPError

@auth.verify_token
def verify_token(token):
    try:
        data = jwt.decode(
            token.encode('ascii'),
            current_app.config['SECRET_KEY'],
        )
        if data["exp"] < int(datetime.now().timestamp()):
            return None
        return data
    except:
        return None

def role_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            user_roles = [item["name"] for item in auth.current_user.get("roles")]
            for role in roles:
                if role in user_roles:
                    return fn(*args, **kwargs)
            raise HTTPError(message="Access denied", status_code=403)
        return decorated_function
    return wrapper


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

from app.blueprints.supplier import bp as bp_supplier
bp.register_blueprint(bp_supplier, url_prefix='/supplier')

from app.models import *