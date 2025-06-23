from flask_login import current_user

from app.blueprints.courier import bp
from app.models.address import Address

from app.models.order import Order, Statuses
from flask import render_template, request, redirect, flash
from app.extensions import db, auth
from app.blueprints import role_required, auth_required
from app.models.phonenumbers import Phonenumber
from sqlalchemy import or_


@bp.route("/", methods=["GET"])
@auth_required(auth)
@role_required(["courier"])
def courier_page():
    # Separate the orders based on the courier's user ID
    my_orders = Order.query.filter_by(courier_id=current_user.courier_id).all()
    other_orders = Order.query.filter(
        or_(
            Order.courier_id != current_user.courier_id,
            Order.courier_id.is_(None)
        )
    ).all()

    statuses = ["DeliveryStarted", "Delivered"]

    phonenumbers = {phonenumber.id: phonenumber for phonenumber in db.session.query(Phonenumber).all()}
    addresses = {address.id: address for address in db.session.query(Address).all()}

    return render_template(
        "courier.html",
        my_orders=my_orders,
        other_orders=other_orders,
        statuses=statuses,
        phonenumbers=phonenumbers,
        addresses=addresses,
        user=current_user
    )



@bp.route("/api/courier/update_order_status", methods=["POST"])
@auth_required(auth)
@role_required(["courier"])
def update_order_status_as_courier():
    order_id = request.form.get("order_id", type=int)
    new_status = request.form.get("new_status")

    print(f"Received data: order_id={order_id}, new_status={new_status}")

    if not order_id or not new_status:
        flash("Order ID or new status is missing.", "error")
        return redirect("/api/courier")

    order = Order.query.get(order_id)

    if not order:
        flash(f"No order found with ID {order_id}.", "error")
        return redirect("/api/courier")

    if not any(new_status == status.value for status in Statuses):
        flash(f"Invalid status selected: {new_status}.", "error")
        return redirect("/api/courier")

    if order.courier_id == None:
        flash(f"Order {order_id} is not assigned to a courier.", "error")
        return redirect("/api/courier")

    try:
        order.status = Statuses(new_status)
        db.session.commit()
        flash(f"Order {order_id}'s status updated successfully to {new_status}.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error updating order status: {str(e)}", "error")

    return redirect("/api/courier")