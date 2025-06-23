from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user

from app import User
from app.extensions import auth, db

from app.blueprints.user import bp
from app.blueprints import role_required, auth_required
from app.models.address import Address

from app.models.item import Item
from app.models.order import Order, Statuses
from app.models.orderitem import OrderItem
from app.models.phonenumbers import Phonenumber


@bp.route("/")
@auth_required(auth)
@role_required(["user"])
def list_items():
    items = Item.query.filter_by(deleted=0).all()
    my_orders = Order.query.filter_by(user_id=current_user.id).all()
    phonenumbers = {
        phonenumber.id: phonenumber for phonenumber in
        db.session.query(Phonenumber).filter(Phonenumber.number.isnot(None)).all()
    }

    addresses = {address.id: address for address in db.session.query(Address).all()}
    return render_template("user.html",
                           items=items,
                           user=current_user,
                           my_orders=my_orders,
                           phonenumbers=phonenumbers,
                           addresses=addresses)


@bp.route("/create_order", methods=["POST"])
@auth_required(auth)
@role_required(["user"])
def create_order():
    if request.method == "POST":
        form_data = request.form.to_dict(flat=False)

        email = form_data.get("email", [None])[0]
        phone_number = form_data.get("phone", [None])[0]
        postal_code = form_data.get("postal_code", [None])[0]
        city = form_data.get("city", [None])[0]
        street = form_data.get("street", [None])[0]

        if not all([email, phone_number, postal_code, city, street]):
            flash("All shipping information fields are required.", "error")
            return redirect(url_for("main.user.list_items"))

        try:
            items = {int(key.replace('items[', '').replace(']', '')): int(value[0])
                     for key, value in form_data.items()
                     if key.startswith('items[') and value[0].strip() and int(value[0]) > 0}

        except ValueError:
            flash("Invalid or missing quantity in one or more selected items.", "error")
            return redirect(url_for("main.user.list_items"))

        if not items:
            flash("All selected quantities are zero. Please select a valid quantity.", "error")
            return redirect(url_for("main.user.list_items"))

        try:
            phone_record = db.session.query(Phonenumber).filter_by(number=phone_number).first()
            if not phone_record:
                phone_record = Phonenumber(number=phone_number)
                db.session.add(phone_record)
                db.session.flush()

            address_record = db.session.query(Address).filter_by(
                postalcode=postal_code, city=city, street=street).first()
            if not address_record:
                address_record = Address(postalcode=postal_code, city=city, street=street)
                db.session.add(address_record)
                db.session.flush()

            new_order = Order(
                user_id=current_user.id,
                phonenumber_id=phone_record.id,
                address_id=address_record.id,
                created_at=datetime.utcnow(),
                status=Statuses.Received,
                email=email
            )
            db.session.add(new_order)
            db.session.flush()

            order_items = []
            for item_id, quantity in items.items():
                item = db.session.query(Item).filter_by(id=item_id).first()

                if not item:
                    flash(f"Item with ID {item_id} not found.", "error")
                    return redirect(url_for("main.user.list_items"))

                if quantity > item.quantity_available:
                    flash(f"Only {item.quantity_available} units of {item.name} are available.", "error")
                    return redirect(url_for("main.user.list_items"))

                item.quantity_available -= quantity
                order_items.append(OrderItem(
                    order_id=new_order.id,
                    item_id=item_id,
                    quantity=quantity
                ))

            db.session.add_all(order_items)
            db.session.commit()

            flash("Your order has been placed successfully!", "success")
            return redirect(url_for("main.user.list_items"))

        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while placing the order: {str(e)}", "error")
            return redirect(url_for("main.user.list_items"))

    return render_template("user.html", user=current_user)



@bp.route("/add_feedback", methods=["POST"])
@auth_required(auth)
@role_required(["user"])
def add_feedback():
    order_id = request.form.get("order_id", type=int)
    feedback = request.form.get("feedback")

    if not order_id or not feedback:
        flash("Missing feedback!", "error")
        return redirect(url_for("main.user.list_items"))

    order = db.session.query(Order).filter_by(id=order_id, user_id=current_user.id).first()

    if not order:
        flash("There is no order with this ID", "error")
        return redirect(url_for("main.user.list_items"))

    if order.status != Statuses.ReceptionConfirmed and order_id == order.id:
        flash("Please confirm the order's reception first.", "error")
        return redirect(url_for("main.user.list_items"))

    try:
        order.feedback = feedback
        db.session.commit()
        flash("Feedback added. Thank you for your purchase", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error saving the feedback: {str(e)}", "error")

    return redirect("/api/user")

@bp.route("/confirm_reception", methods=["POST"])
@auth_required(auth)
@role_required(["user"])
def confirm_reception():
    order_id = request.form.get("order_id", type=int)
    if not order_id:
        flash("Missing order id", "error")
        return redirect(url_for("main.user.list_items"))
    order = db.session.query(Order).filter_by(id=order_id).first()
    if not order:
        flash("Order not found", "error")
    try:
        order.status = Statuses.ReceptionConfirmed
        db.session.commit()
        flash("Order confirmed", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error updating order status: {str(e)}", "error")
    return redirect("/api/user")