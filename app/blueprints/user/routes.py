from flask import jsonify
from app.blueprints.user import bp
from app.blueprints.user.schemas import UserResponseSchema, UserRequestSchema, AddressSchema, UserLoginSchema
from app.blueprints.user.service import UserService
from apiflask import HTTPError
from apiflask.fields import String, Email, Nested, Integer, List


@bp.route('/')

def index():
    return 'This is The User Blueprint'


@bp.post('/registrate')
@bp.doc(tags=["user"])
@bp.input(UserRequestSchema, location="json")
@bp.output(UserResponseSchema)
def user_registrate(json_data):
    success, response = UserService.user_registrate(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.post('/login')
@bp.doc(tags=["user"])
@bp.input(UserLoginSchema, location="json")
@bp.output(UserResponseSchema)
def user_login(json_data):
    success, response = UserService.user_login(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

