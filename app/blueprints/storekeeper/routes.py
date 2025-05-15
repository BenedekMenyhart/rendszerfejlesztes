from flask import render_template, redirect, url_for, flash, request
from app.blueprints.storekeeper import bp
from app.extensions import db
from app.models.courier import Courier
from app.models.shipment import Shipment
from app.models.shipmentitem import ShipmentItem
from app.models.order import Order, Statuses
from app.models.item import Item


@bp.route('/')
def storekeeper_index():
    try:
        items = db.session.query(Item).filter(Item.deleted.is_(0)).all()
        orders = db.session.query(Order).all()
        shipments = db.session.query(Shipment).all()
        shipmentitems = db.session.query(ShipmentItem).all()
        couriers = db.session.query(Courier).all()
    except LookupError as e:
        flash(str(e), 'error')
        orders = []
        shipments = []
        shipmentitems = []
    return render_template("storekeeper.html",items=items, orders=orders, shipments=shipments, shipmentitems=shipmentitems, couriers=couriers)


@bp.route('/process_shipment', methods=['GET', 'POST'])
def process_shipment():

    shipment_id = request.form.get("shipment_id", type=int)
    if not shipment_id:
        flash("Invalid Shipment ID.", "error")
        return redirect(url_for("main.storekeeper.storekeeper_index"))

    shipment = db.session.query(Shipment).filter_by(id=shipment_id).first()

    if not shipment:
        flash(f"Shipment with ID {shipment_id} does not exist.", "error")
        return redirect(url_for("main.storekeeper.storekeeper_index"))

    if shipment.received:
        flash(f"Shipment with ID {shipment_id} has already been processed.", "info")
        return redirect(url_for("main.storekeeper.storekeeper_index"))

    try:
        for shipment_item in shipment.items:
            item = db.session.query(Item).filter_by(id=shipment_item.item_id).first()
            if item:
                item.quantity_available += shipment_item.quantity
                db.session.add(item)

        shipment.received = True
        db.session.add(shipment)
        db.session.commit()

        flash(f"Shipment with ID {shipment_id} processed successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while processing shipment: {str(e)}", "error")

    return redirect(url_for("main.storekeeper.storekeeper_index"))

@bp.route('/update_order_status', methods=['POST'])
def update_order_status():
    order_id = request.form.get("order_id", type=int)
    status = request.form.get("status")

    if not order_id or not status:
        flash("Order ID or Status is missing.", "error")
        return redirect(url_for("main.storekeeper.storekeeper_index"))

    order = db.session.query(Order).filter_by(id=order_id).first()
    if not order:
        flash(f"Order with ID {order_id} does not exist.", "error")
        return redirect(url_for("main.storekeeper.storekeeper_index"))

    try:
        order.status = status
        db.session.add(order)
        db.session.commit()
        flash(f"Order with ID {order_id} updated to status '{status}'.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while updating the order status: {str(e)}", "error")

    return redirect(url_for("main.storekeeper.storekeeper_index"))


@bp.route('/sign_courier_to_order', methods=['POST'])
def sign_courier_to_order():

    order_id = request.form.get("order_id", type=int)
    courier_id = request.form.get("courier_id", type=int)


    if not order_id or not courier_id:
        flash("Order ID and Courier ID are required.", "error")
        return redirect(url_for("main.storekeeper.storekeeper_index"))


    order = db.session.query(Order).filter_by(id=order_id).first()
    if not order:
        flash(f"Order with ID {order_id} does not exist.", "error")
        return redirect(url_for("main.storekeeper.storekeeper_index"))


    if order.status not in [Statuses.Received, Statuses.Processing, Statuses.Processed]:
        flash(f"Order with ID {order_id} cannot be assigned to a courier. Current status: {order.status}", "error")
        return redirect(url_for("main.storekeeper.storekeeper_index"))


    courier = db.session.query(Courier).filter_by(id=courier_id).first()
    if not courier:
        flash(f"Courier with ID {courier_id} does not exist.", "error")
        return redirect(url_for("main.storekeeper.storekeeper_index"))


    try:
        order.courier_id = courier_id
        order.status = Statuses.AssignedToCourier.value
        db.session.add(order)
        db.session.commit()
        flash(f"Order with ID {order_id} successfully assigned to Courier ID {courier_id}.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while assigning the courier: {str(e)}", "error")

    return redirect(url_for("main.storekeeper.storekeeper_index"))