#from flask import Blueprint
from apiflask import APIBlueprint

bp = APIBlueprint('courier', __name__, tag="courier")

from app.blueprints.courier import routes