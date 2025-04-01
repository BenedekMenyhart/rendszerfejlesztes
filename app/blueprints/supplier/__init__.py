#from flask import Blueprint
from apiflask import APIBlueprint

bp = APIBlueprint('supplier', __name__, tag="supplier")

from app.blueprints.supplier import routes