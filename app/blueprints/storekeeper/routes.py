from flask import render_template, redirect, url_for, flash
from app.blueprints.storekeeper import bp
from app.extensions import db
from app.models.shipment import Shipment
from app.models.shipmentitem import ShipmentItem
from app.models.order import Order, Statuses
from app.models.user import User
from app.models.role import Role
from collections import defaultdict

from collections import defaultdict


@bp.route('/')
def storekeeper_index():
    try:
        orders = db.session.query(Order).all()
        shipments = db.session.query(Shipment).all()
        shipmentitems = db.session.query(ShipmentItem).all()


    except LookupError as e:
        flash(str(e), 'error')
        orders = []
    return render_template("storekeeper.html", orders=orders, shipments=shipments, shipmentitems=shipmentitems)
