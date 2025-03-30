from apiflask import APIBlueprint
bp = APIBlueprint('user', __name__, tag="user")

from app.blueprints.user import routes