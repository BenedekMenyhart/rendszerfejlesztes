from app.blueprints import role_required
from app.blueprints.courier import bp
from app.blueprints.courier.service import CourierService
from flask import render_template
from app.blueprints.order.schemas import OrderResponseSchema
from app.blueprints.courier.service import CourierService
from apiflask.fields import String, Integer
from apiflask import HTTPError

from app.extensions import auth

from app.models.order import Order, Statuses
from flask import render_template, request, redirect, flash
from app.extensions import db


@bp.route("/", methods=["GET"])
def courier_page():
    # Fetch all orders from the database
    orders = Order.query.all()

    # Fetch all possible statuses from the Statuses enum
    all_statuses = [status.value for status in Statuses]

    # Render the courier template with the orders and statuses
    return render_template("courier.html", orders=orders, statuses=all_statuses)


@bp.route("/api/courier/update_order_status", methods=["POST"])
def update_order_status_as_courier():
    # Extract data from the form
    order_id = request.form.get("order_id", type=int)
    new_status = request.form.get("new_status")

    # Debug: Log the received data
    print(f"Received data: order_id={order_id}, new_status={new_status}")

    if not order_id or not new_status:
        flash("Order ID or new status is missing.", "error")
        return redirect("/api/courier")

    # Fetch the order from the database
    order = Order.query.get(order_id)

    if not order:
        flash(f"No order found with ID {order_id}.", "error")
        return redirect("/api/courier")

    # Validate new_status against the Statuses enum
    if not any(new_status == status.value for status in Statuses):
        flash(f"Invalid status selected: {new_status}.", "error")
        return redirect("/api/courier")

    try:
        # Update the status of the order
        order.status = Statuses(new_status)
        db.session.commit()  # Save changes to the database
        flash(f"Order {order_id}'s status updated successfully to {new_status}.", "success")
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        flash(f"Error updating order status: {str(e)}", "error")

    # Redirect back to the main courier page
    return redirect("/api/courier")