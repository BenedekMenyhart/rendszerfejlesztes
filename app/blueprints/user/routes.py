from datetime import datetime

from flask import jsonify, render_template, flash, redirect, url_for, request
from flask_login import current_user

from app import User
from app.extensions import auth, db
from app.blueprints import role_required
from app.blueprints.user import bp
from app.blueprints.user.schemas import UserResponseSchema, UserRequestSchema, UserLoginSchema, RoleSchema, AddressSchema
from app.blueprints.user.service import UserService
from apiflask import HTTPError
from apiflask.fields import String, Email, Nested, Integer, List

from app.models.item import Item
from app.models.order import Order, Statuses
from app.models.orderitem import OrderItem


@bp.route("/")
def list_items():
    items = Item.query.filter_by(deleted=0).all()
    return render_template("user.html", items=items)


@bp.post('/registrate')
@bp.doc(tags=["user"])
@bp.input(UserRequestSchema, location="json")
@bp.output(UserResponseSchema)
def user_registrate(json_data):
    success, response = UserService.user_registrate(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)



@bp.get('/roles')
@bp.output(RoleSchema(many=True))
@bp.auth_required(auth)
@role_required(["User"])
def user_list_roles():
    success, response = UserService.user_list_roles()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/myroles')
@bp.doc(tags=["user"])
@bp.output(RoleSchema(many=True))
@bp.auth_required(auth)
@role_required(["User"])
def user_list_user_roles():
    success, response = UserService.list_user_roles(auth.current_user.get("user_id"))
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.route('/update_contact_info', methods=['POST'])
def update_contact_info():
    field = request.form.get("field")
    new_value = request.form.get("new_value")
    username = request.form.get("username")

    if not field or not new_value or not username:
        flash("Hiányzó mezők a kérésben.", "error")
        return redirect(url_for("main.user.list_items"))  # Itt állítsd be a megfelelő céloldalt

    user = db.session.query(User).filter_by(name=username).first()
    if not user:
        flash(f"A(z) {username} nevű felhasználó nem található.", "error")
        return redirect(url_for("main.user.list_items"))

    try:
        if field == "email":
            user.email = new_value
        elif field == "phone":
            user.phone = new_value
        else:
            flash("Érvénytelen mezőt próbáltál frissíteni.", "error")
            return redirect(url_for("main.user.list_items"))

        db.session.add(user)
        db.session.commit()
        flash(f"Sikeres frissítés: {field} -> {new_value}", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Hiba történt a frissítés során: {str(e)}", "error")

    return redirect(url_for("main.user.list_items"))

@bp.route("/create_order", methods=["GET", "POST"])
def create_order():
    if request.method == "POST":
        item_id = request.form.get("item_id", type=int)
        quantity = request.form.get("quantity", type=int)

        if not item_id or not quantity:
            flash("Kérlek, töltsd ki az összes mezőt!", "error")
            return redirect(url_for("main.user.create_order"))

        item = db.session.query(Item).filter_by(id=item_id).first()
        if not item:
            flash("A megadott termék nem létezik.", "error")
            return redirect(url_for("main.user.create_order"))

        if quantity > item.quantity_available:
            flash(f"Csak {item.quantity_available} darab elérhető ebből a termékből.", "error")
            return redirect(url_for("main.user.create_order"))

        item.quantity_available -= quantity
        db.session.commit()

        try:
            new_order = Order(
                user_id=current_user.id,
                address_id=current_user.address_id,
                created_at=datetime.utcnow().isoformat(),
                status="Received"
            )
            db.session.add(new_order)
            db.session.flush()

            order_item = OrderItem(
                order_id=new_order.id,
                item_id=item_id,
                quantity=quantity
            )
            db.session.add(order_item)
            db.session.commit()

            flash("Sikeresen leadtad a rendelést!", "success")
            return redirect(url_for("main.user.list_items"))

        except Exception as e:
            db.session.rollback()
            flash(f"Hiba történt a rendelés során: {str(e)}", "error")
            return redirect(url_for("main.user.create_order"))

    return render_template("user.html")

@bp.route("/add_feedback", methods=["POST"])
def add_feedback():
    order_id = request.form.get("order_id", type=int)
    feedback = request.form.get("feedback")

    if not order_id or not feedback:
        flash("Hiányzó adat!", "error")
        return redirect(url_for("main.user.list_items"))

    # Keresd meg a rendelést az ID és a felhasználó alapján
    order = db.session.query(Order).filter_by(id=order_id, user_id=current_user.id).first()

    if not order:
        flash("A rendelés nem található.", "error")
        return redirect(url_for("main.user.list_items"))

    if order.status != Statuses.ReceptionConfirmed and order_id == order.id:
        flash("Megjegyzést csak akkor adhatsz hozzá, ha a rendelés státusza 'Reception_confirmed'.", "error")
        return redirect(url_for("main.user.list_items"))

    try:
        order.feedback = feedback
        db.session.commit()
        flash("Megjegyzés sikeresen elmentve.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Hiba történt mentés közben: {str(e)}", "error")

    return render_template("user.html")