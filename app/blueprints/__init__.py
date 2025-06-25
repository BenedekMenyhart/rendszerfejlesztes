#from flask import Blueprint
from apiflask import APIBlueprint
from sqlalchemy import func, and_
from app.forms.registrationForm import RegistrationForm
from app.models.address import Address
from app.models.phonenumbers import Phonenumber
from app.models.role import Role
bp = APIBlueprint('main', __name__, tag="default")
from functools import wraps
from app.extensions import auth, db
from flask import current_app, session, request
from authlib.jose import jwt
from datetime import datetime
from apiflask import HTTPError
from flask import render_template, flash, redirect, url_for
from app.forms.loginForm import LoginForm
from flask_login import login_user, current_user
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import time
from flask import jsonify
from flask_login import logout_user
from flask import session, redirect, url_for, flash
from flask_login import logout_user, current_user
from functools import wraps


@bp.app_context_processor
def inject_user_roles():
    if current_user.is_authenticated:
        roles = [role.name for role in current_user.roles]
    else:
        roles = []
    return {'roles': roles}


@auth.verify_token
def verify_token(token):
    try:
        data = jwt.decode(
            token.encode('ascii'),
            current_app.config['SECRET_KEY'],
        )
        if data["exp"] < int(datetime.now().timestamp()):
            return None
        return data
    except:
        return None

def role_required(allowed_roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            user_roles = [role.name.lower() for role in current_user.roles]
            normalized_allowed_roles = [role.lower() for role in allowed_roles]

            if not any(role in user_roles for role in normalized_allowed_roles):
                logout_user()
                session.clear()
                session["_flashes"] = [("__flashes", "Permission denied! You have been logged out!", "error")]
                return redirect(url_for("main.index"))

            return fn(*args, **kwargs)
        return decorated_function
    return wrapper



def auth_required(auth):
    def wrapper(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Please log in!", "error")
                return redirect(url_for("main.login"))
            return fn(*args, **kwargs)
        return decorated_function
    return wrapper

@bp.route('/')
def index():
    return render_template('starter.html', title='Starter page')

@bp.route('/index')
@auth_required(auth)
def index2():
    user=current_user
    return render_template('index.html',  title='Index page', user=user)


@bp.route('/logout')
@auth_required(auth)
def logout():
    logout_user()
    session.clear()
    flash("Successful logout!")
    return redirect(url_for('main.index'))



@bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "GET":
        return render_template("login.html", title="Login", form=form)


    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()

        if user:
            if user.check_password(form.password.data):
                token_data = {
                    "sub": user.name,
                    "id": user.id,
                    "courier_id": user.courier_id,
                    "roles": [{"name": role.name} for role in user.roles],
                    "exp": int(time.time()) + 3600  # Token lejárati idő (1 óra)
                }

                # JWT token generálása
                token = jwt.encode(
                    {"alg": "HS256"},
                    token_data,
                    current_app.config['SECRET_KEY']
                )


                login_user(user)
                flash("Login successful!")


                roles = [role.name for role in user.roles]

                if len(roles) == 1:
                    if roles[0] == "user":
                        return redirect("/api/user")
                    elif roles[0] == "courier":
                        return redirect("/api/courier")
                    elif roles[0] == "storekeeper":
                        return redirect("/api/storekeeper")
                    elif roles[0] == "supplier":
                        return redirect("/api/supplier")

                return render_template('index.html', roles=roles, user=user, title='Index page')

            else:
                flash("Invalid username or password. Please try again!")
                return redirect(url_for("main.login"))

    # Ha a POST kérés nem valid (pl. adatokat nem adtak meg)
    return render_template("login.html", title="Login", form=form)


def get_address_id(postalcode, city, street):
    address = Address.query.filter(
        and_(
            Address.postalcode == postalcode,
            Address.city == city,
            Address.street == street
        )
    ).first()

    if address:
        return address.id
    else:
        return None

def get_phone_id(number):
    phonenumber = Phonenumber.query.filter_by(number=number).first()
    if phonenumber:
        return phonenumber.id
    else:
        return None


@bp.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user:
            flash(f"Username: {form.name.data} has been taken.", "error")
            return render_template("register.html", title="Register", form=form)

        default_role = Role.query.filter_by(id=1).first()
        if not default_role:
            flash("Default role with ID 1 is not found in the database.", "error")
            return render_template("register.html", title="Register", form=form)

        address_id = get_address_id(
            form.postalcode.data,
            form.city.data,
            form.street.data
        )
        if not address_id:
            max_address_id = db.session.query(func.max(Address.id)).scalar() or 0
            new_address = Address(
                id=max_address_id + 1,
                postalcode=form.postalcode.data,
                city=form.city.data,
                street=form.street.data
            )
            db.session.add(new_address)
            db.session.commit()
            address_id = new_address.id

        phone_id = get_phone_id(form.phone.data)
        if not phone_id:
            max_phone_id = db.session.query(func.max(Phonenumber.id)).scalar() or 0
            new_phone = Phonenumber(
                id=max_phone_id + 1,
                number=form.phone.data
            )
            db.session.add(new_phone)
            db.session.commit()
            phone_id = new_phone.id

        hashed_password = generate_password_hash(form.password.data)

        max_user_id = db.session.query(func.max(User.id)).scalar() or 0
        new_user = User(
            id=max_user_id + 1,
            name=form.name.data,
            email=form.email.data,
            password=hashed_password,
            phonenumber_id=phone_id,
            address_id=address_id,
            courier_id=None
        )

        new_user.roles.append(default_role)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please log in.")
            return redirect(url_for("main.login"))

        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred during registration: {str(e)}", "error")

    return render_template("register.html", title="Register", form=form)


@bp.route('/update_contact_info', methods=['POST'])
@auth_required(auth)
def update_contact_info():
    if request.method == "POST":
        form_data = request.form.to_dict(flat=False)

        email = form_data.get("email", [None])[0]
        phone_number = form_data.get("phone", [None])[0]
        postal_code = form_data.get("postal_code", [None])[0]
        city = form_data.get("city", [None])[0]
        street = form_data.get("street", [None])[0]
        password = form_data.get("password", [None])[0]
        password2 = form_data.get("password2", [None])[0]

        if email:
            modifiable=True
        elif phone_number:
            modifiable=True
        elif postal_code:
            modifiable=True
        elif city:
            modifiable=True
        elif street:
            modifiable=True
        elif password:
            modifiable = True
        else:
            modifiable=False

        if not modifiable:
            flash("You have to update a valid field.", "error")
            return redirect(url_for("main.index2", user=current_user))


        user = db.session.query(User).filter_by(id=current_user.id).first()
        if not user:
            flash(f"User with {current_user.name} name is invalid.", "error")
            return redirect(url_for("main.index2", user=current_user))

        try:
            if email and email != user.email:
                user.email = email

            if phone_number and user.phonenumber.number != phone_number:
                user.phonenumber.number = phone_number

            if password:
                if user.check_password(password):
                    flash("You can't modify your password without entering a new one.", "error")
                    return redirect(url_for("main.index2", user=current_user))
                else:
                    if password == password2:
                        user.set_password(password)
                    else:
                        flash("Your new password and confirmation don't match!", "error")
                        return redirect(url_for("main.index2", user=current_user))


            if (postal_code and postal_code != user.address.postalcode) and (city and city != user.address.city):
                user.address.postalcode = postal_code
                user.address.city = city
            elif postal_code and not city:
                flash("You can't modify your postal code without changing the town's name.", "error")
                return redirect(url_for("main.index2", user=current_user))
            elif city and not postal_code:
                flash("You can't modify your town's name without changing the postal code.", "error")
                return redirect(url_for("main.index2", user=current_user))

            if street:
                if postal_code and city:
                    user.address.street = street
                elif user.address.street != street:
                    user.address.street = street
                else:
                    flash("You can't modify your street address without changing the postal code and/or town's name.", "error")
                    return redirect(url_for("main.index2", user=current_user))


            db.session.add(user)
            db.session.commit()
            flash(f"Successful modification", "success")

        except Exception as e:
            db.session.rollback()
            flash(f"Error during update: {str(e)}", "error")

    return redirect("/api/index")

#register blueprints here
from app.blueprints.user import bp as bp_user
bp.register_blueprint(bp_user, url_prefix='/user')


from app.blueprints.storekeeper import bp as bp_storekeeper
bp.register_blueprint(bp_storekeeper, url_prefix='/storekeeper')

from app.blueprints.courier import bp as bp_courier
bp.register_blueprint(bp_courier, url_prefix='/courier')


from app.blueprints.supplier import bp as bp_supplier
bp.register_blueprint(bp_supplier, url_prefix='/supplier')

from app.models import *