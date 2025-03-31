#from flask import Blueprint
from apiflask import APIBlueprint

bp = APIBlueprint('storekeeper', __name__, tag="storekeeper")

from app.blueprints.storekeeper import routes