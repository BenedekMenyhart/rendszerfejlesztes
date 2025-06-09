from flask import render_template, redirect, url_for, flash, request
from sqlalchemy import and_, func

from app.models.role import Role
from app.models.user import User
from app.blueprints.storekeeper import bp
from app.extensions import db
from app.models.courier import Courier
from app.models.shipment import Shipment
from app.models.shipmentitem import ShipmentItem
from app.models.order import Order, Statuses
from app.models.item import Item
from app.models.address import Address
from app.forms.newItemForm import NewItemForm


@bp.route('/')
def storekeeper_index():
    try:
        items = db.session.query(Item).filter(Item.deleted.is_(0)).all()
        orders = db.session.query(Order).all()
        shipments = db.session.query(Shipment).all()
        shipmentitems = db.session.query(ShipmentItem).all()
        couriers = db.session.query(Courier).all()
        addresses = {address.id: address for address in db.session.query(Address).all()}
        users = db.session.query(User).all()
        roles = db.session.query(Role).all()

        form = NewItemForm()

        available_roles = {
            user.id: set(roles) - set(user.roles)
            for user in users
        }

    except LookupError as e:
        flash(str(e), 'error')
        orders = []
        shipments = []
        shipmentitems = []
        addresses = {}
        users = []
        roles = []
        form = None
        available_roles = {}

    return render_template("storekeeper.html",
                           items=items,
                           orders=orders,
                           shipments=shipments,
                           shipmentitems=shipmentitems,
                           couriers=couriers,
                           addresses=addresses,
                           users=users,
                           roles=roles,
                           available_roles=available_roles,
                           form=form)



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

        if status == Statuses.Received.value or status == Statuses.Processing.value or status == Statuses.Processed.value:
            order.courier_id = None

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

def check_if_item_exists(item_name):
    item = Item.query.filter(
        and_(
            Item.name == item_name
        )
    ).first()

    if item:
        return item
    else:
        return None

@bp.route('/add_new_item', methods=["GET", "POST"])
def add_new_item():
    form = NewItemForm()
    if form.validate_on_submit():
        item_name = form.item_name.data

        item = check_if_item_exists(item_name)

        if item:
            if item.deleted==1:
                item.deleted=0
                item.description=form.description.data
                item.price=form.price.data
                item.quantity_available=0
                db.session.add(item)
                db.session.commit()
                flash("Item is successfully restored and updated from the database!")
            else:
                flash("Item already exists.", "error")
        else:
            description = form.description.data
            price = form.price.data

            max_item_id = db.session.query(func.max(Item.id)).scalar() or 0

            new_item = Item(
                id=max_item_id + 1,
                name=item_name,
                description=description,
                price=price,
                quantity_available=0,
                deleted=0
            )
            try:
                db.session.add(new_item)
                db.session.commit()
                flash("New item successfully added to the database!")

            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred during adding the new item: {str(e)}", "error")

    return redirect(url_for("main.storekeeper.storekeeper_index"))

@bp.route('/delete_item', methods=['POST'])
def delete_item():
    item_id = request.form.get("item_id", type=int)
    if not item_id:
        flash("Invalid Item ID.", "error")
        return redirect(url_for("main.storekeeper.storekeeper_index"))
    else:
        item = db.session.query(Item).filter_by(id=item_id).first()
        if not item:
            flash(f"Item with ID {item_id} does not exist.", "error")
        else:
            try:
                item.deleted = 1
                db.session.add(item)
                db.session.commit()
                flash(f"Item with ID {item_id} deleted successfully.", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred while deleting the item: {str(e)}", "error")
        return redirect(url_for("main.storekeeper.storekeeper_index"))

@bp.route('/assign_role', methods=['POST'])
def assign_role():
    user_id = request.form.get("user_id", type=int)
    role_id = request.form.get("role_id", type=int)

    if not user_id or not role_id:
        flash("Invalid user or role ID.", "error")
        return redirect(url_for("main.storekeeper.storekeeper_index"))

    user = db.session.query(User).filter_by(id=user_id).first()
    role = db.session.query(Role).filter_by(id=role_id).first()

    if not user or not role:
        flash("Invalid user or role.", "error")
        return redirect(url_for("main.storekeeper.storekeeper_index"))

    try:
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()
        flash(f"Role '{role.name}' successfully assigned to user '{user.name}'.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while assigning the role: {str(e)}", "error")

    return redirect(url_for("main.storekeeper.storekeeper_index"))

@bp.route('/remove_role', methods=['POST'])
def remove_role():
    user_id = request.form.get("user_id", type=int)
    role_id = request.form.get("role_id", type=int)
    if not user_id or not role_id:
        flash("Invalid user or role ID.", "error")
        return redirect(url_for("main.storekeeper.storekeeper_index"))
    else:
        user = db.session.query(User).filter_by(id=user_id).first()
        role = db.session.query(Role).filter_by(id=role_id).first()
        if not user or not role:
            flash("Invalid user or role.", "error")
            return redirect(url_for("main.storekeeper.storekeeper_index"))
        try:
            user.roles.remove(role)
            db.session.add(user)
            db.session.commit()
            flash(f"Role '{role.name}' successfully removed from user '{user.name} (id={user.id})'.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while removing the role: {str(e)}", "error")
        return redirect(url_for("main.storekeeper.storekeeper_index"))