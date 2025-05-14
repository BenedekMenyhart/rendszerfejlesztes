from flask import render_template, request, flash, redirect

from app.blueprints import role_required
from app.blueprints.supplier import bp
from app.blueprints.courier.service import CourierService

from app.blueprints.order.schemas import OrderResponseSchema
from app.blueprints.courier.service import CourierService
from apiflask.fields import String, Integer
from apiflask import HTTPError

from app.blueprints.shipment.schemas import ShipmentResponseSchema
from app.blueprints.supplier.schemas import FewItemResponseSchema
from app.blueprints.supplier.service import SupplierService
from app.extensions import auth, db
from app.models.item import Item
from app.models.shipment import Shipment
from app.models.shipmentitem import ShipmentItem

"""
@bp.route('/')
def supplier_index():
    return render_template('supplier.html', title='Supplier\'s page')


@bp.get("/items/few/<int:iid>")
@bp.output(FewItemResponseSchema(many = True))
@bp.auth_required(auth)
@role_required(["Supplier"])
def supplier_orders_list_few(iid):
    success, response = SupplierService.items_list_few(iid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get("/items/shipment/<int:iid>/<int:sid>")
@bp.output(ShipmentResponseSchema(many = True))
@bp.auth_required(auth)
@role_required(["Supplier"])
def shipment_add(iid, sid):
    success, response = SupplierService.shipment_add(iid, sid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)
"""

@bp.route('/')
def supplier_index():
    # Fetch items to be shipped
    items = Item.query.all()
    return render_template('supplier.html', title="Supplier's page", items=items)

# Route for submitting shipment data via the form
@bp.route('/api/supplier/submit_shipment_form', methods=['POST'])
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

        item.quantity_available += shipment_quantity


        try:
            db.session.commit()
            flash('Shipment successfully created.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while saving the shipment: {str(e)}', 'error')

        return redirect('/api/supplier')


@bp.get('/items/few/<int:iid>')
@bp.output(FewItemResponseSchema(many=True))
@bp.auth_required(auth)
@role_required(['Supplier'])
def supplier_orders_list_few(iid):
    success, response = SupplierService.items_list_few(iid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/items/shipment/<int:iid>/<int:sid>')
@bp.output(ShipmentResponseSchema(many=True))
@bp.auth_required(auth)
@role_required(['Supplier'])
def shipment_add(iid, sid):
    success, response = SupplierService.shipment_add(iid, sid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

