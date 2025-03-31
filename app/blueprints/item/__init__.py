#from flask import Blueprint
from apiflask import APIBlueprint

bp = APIBlueprint('item', __name__, tag="item")

from app.blueprints.item import routes