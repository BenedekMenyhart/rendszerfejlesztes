from flask import jsonify, render_template

from app.extensions import auth
from app.blueprints import role_required
from app.blueprints.user import bp
from app.blueprints.user.schemas import UserResponseSchema, UserRequestSchema, UserLoginSchema, RoleSchema, AddressSchema
from app.blueprints.user.service import UserService
from apiflask import HTTPError
from apiflask.fields import String, Email, Nested, Integer, List


@bp.route('/')
def user_index():
    return render_template('user.html',  title='User\'s page')


@bp.post('/registrate')
@bp.doc(tags=["user"])
@bp.input(UserRequestSchema, location="json")
@bp.output(UserResponseSchema)
def user_registrate(json_data):
    success, response = UserService.user_registrate(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)



@bp.get('/roles')
@bp.output(RoleSchema(many=True))
@bp.auth_required(auth)
@role_required(["User"])
def user_list_roles():
    success, response = UserService.user_list_roles()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/myroles')
@bp.doc(tags=["user"])
@bp.output(RoleSchema(many=True))
@bp.auth_required(auth)
@role_required(["User"])
def user_list_user_roles():
    success, response = UserService.list_user_roles(auth.current_user.get("user_id"))
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

