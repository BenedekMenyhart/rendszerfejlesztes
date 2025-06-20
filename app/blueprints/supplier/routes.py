from flask import render_template, request, flash, redirect

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

@bp.route('/api/supplier/submit_shipment_form', methods=['POST'])
@auth_required(auth)
@role_required(["supplier"])
def submit_shipment_form():
        # Get form data
        item_id = request.form.get('item_id', type=int)
        delivery_date = request.form.get('delivery_date')
        shipment_quantity = request.form.get('shipment_quantity', type=int)

        if not item_id or not delivery_date or not shipment_quantity:
            flash('Invalid form submission. Please fill out all fields.', 'error')
            return redirect('/api/supplier')

        item = Item.query.get(item_id)
        if not item:
            flash(f'Item with ID {item_id} not found.', 'error')
            return redirect('/api/supplier')


        shipment = Shipment(
            expected_at=delivery_date,
            received=False
        )
        db.session.add(shipment)
        db.session.flush()

        shipment_item = ShipmentItem(
            shipment_id=shipment.id,
            item_id=item_id,
            quantity=shipment_quantity,
        )
        db.session.add(shipment_item)



        try:
            db.session.commit()
            flash('Shipment successfully created.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while saving the shipment: {str(e)}', 'error')

        return redirect('/api/supplier')




