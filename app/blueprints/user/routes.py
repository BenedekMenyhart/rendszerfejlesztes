from flask import jsonify
from app.blueprints.user import bp
#from app.blueprints.user.schemas import UserResponseSchema, UserRequestSchema, AddressSchema, UserLoginSchema
#from app.blueprints.user.service import UserService
from apiflask import HTTPError
from apiflask.fields import String, Email, Nested, Integer, List


@bp.route('/')

def index():
    return 'This is The User Blueprint'