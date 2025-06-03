from app.blueprints.courier import bp
from app.models.address import Address

from app.models.order import Order, Statuses
from flask import render_template, request, redirect, flash
from app.extensions import db


@bp.route("/", methods=["GET"])
def courier_page():
    orders = Order.query.all()

    all_statuses = [status.value for status in Statuses]

    addresses = {address.id: address for address in db.session.query(Address).all()}

    return render_template("courier.html", orders=orders, statuses=all_statuses, addresses=addresses)


@bp.route("/api/courier/update_order_status", methods=["POST"])
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

    try:
        order.status = Statuses(new_status)
        db.session.commit()
        flash(f"Order {order_id}'s status updated successfully to {new_status}.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error updating order status: {str(e)}", "error")

    return redirect("/api/courier")