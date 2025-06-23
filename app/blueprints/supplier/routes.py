from flask import render_template, request, flash, redirect, url_for

from flask_login import current_user
from app.blueprints.supplier import bp
from apiflask import HTTPError
from app.extensions import auth, db
from app.models.item import Item
from app.models.shipment import Shipment
from app.models.shipmentitem import ShipmentItem
from app.blueprints import role_required, auth_required


@bp.route('/')
@auth_required(auth)
@role_required(["supplier"])
def supplier_index():
    items = Item.query.all()
    return render_template('supplier.html', title="Supplier's page", items=items, user=current_user)

@bp.route('/submit_shipment', methods=['POST'])
@auth_required(auth)
@role_required(["supplier"])
def submit_shipment():
    form_data = request.form.to_dict(flat=False)
    delivery_date = form_data.get("delivery_date", [None])[0]

    if not delivery_date:
        flash("Expected delivery date is missing.", "error")
        return redirect(url_for("main.supplier.supplier_index"))

    try:
        items = {int(key.replace('items[', '').replace(']', '')): int(value[0])
                 for key, value in form_data.items()
                 if key.startswith('items[') and value[0].strip() and int(value[0]) > 0}
    except ValueError:
        flash("Invalid or missing quantity in one or more selected items.", "error")
        return redirect(url_for("main.supplier.supplier_index"))

    if not items:
        flash("No valid items selected for shipment.", "error")
        return redirect(url_for("main.supplier.supplier_index"))

    try:
        new_shipment = Shipment(
            expected_at=delivery_date,
            received=False
        )
        db.session.add(new_shipment)
        db.session.flush()

        shipment_items = []

        for item_id, quantity in items.items():
            item = db.session.query(Item).filter_by(id=item_id).first()

            if not item:
                flash(f"Item with ID {item_id} not found.", "error")
                continue

            item.requested = update_requested_quantity(item.requested, quantity)
            db.session.add(item)

            shipment_items.append(ShipmentItem(
                shipment_id=new_shipment.id,
                item_id=item_id,
                quantity=quantity
            ))

        db.session.add_all(shipment_items)
        db.session.commit()
        flash("Shipment successfully submitted.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {str(e)}", "error")

    return redirect(url_for("main.supplier.supplier_index"))


def update_requested_quantity(current_requested, shipped_quantity):
    if not current_requested or current_requested == 0:
        return 0

    if shipped_quantity >= current_requested:
        return 0

    return current_requested - shipped_quantity



