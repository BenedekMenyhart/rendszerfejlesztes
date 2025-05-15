#from flask import Blueprint
from apiflask import APIBlueprint
from sqlalchemy import func

from app.forms.registrationForm import RegistrationForm
from app.models.role import Role

bp = APIBlueprint('main', __name__, tag="default")
from functools import wraps
from app.extensions import auth, db
from flask import current_app, render_template, session
from authlib.jose import jwt
from datetime import datetime
from apiflask import HTTPError
from flask import render_template
from app.forms.loginForm import LoginForm
from flask import render_template, flash, redirect, url_for
from app.forms.loginForm import LoginForm
from flask_login import login_user, current_user
from app.models.user import User

from werkzeug.security import check_password_hash
import time
from flask import g
@bp.app_context_processor
def inject_user_roles():
    roles = [role["name"] for role in auth.current_user.get("roles", [])] if auth.current_user else []
    return dict(user_roles=roles)

@bp.app_context_processor
def inject_user_roles():
    if current_user.is_authenticated:
        roles = [role.name for role in current_user.roles]  # Lekérdezzük a "Role" táblából
    else:
        roles = []
    return {'user_roles': roles}

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

def role_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            user_roles = [item["name"] for item in auth.current_user.get("roles")]
            for role in roles:
                if role in user_roles:
                    return fn(*args, **kwargs)
            raise HTTPError(message="Access denied", status_code=403)
        return decorated_function
    return wrapper


@bp.route('/')
def index():
    return render_template('base.html',  title='Base page')

@bp.route('/index')
def index2():
    return render_template('index.html',  title='Base page')


@bp.route('/logout')
def logout():
    if auth.current_user:
        auth.current_user = None
    session.clear()
    return redirect(url_for('main.index'))


@bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user and user.password == form.password.data:
            token_data = {
                "sub": user.name,
                "id": user.id,
                "roles": [{"name": role.name} for role in user.roles],
                "exp": int(time.time()) + 3600
            }

            token = jwt.encode(
                {"alg": "HS256"},
                token_data,
                current_app.config['SECRET_KEY']
            )

            login_user(user)
            flash("Sikeres bejelentkezés!")
            return render_template('index.html',  title='Index page')

        else:
            flash("Helytelen felhasználónév vagy jelszó!")

    return render_template("login.html",
                         title="Bejelentkezés",
                         form=form
                         )

@bp.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("Email already registered.")
            return render_template("register.html", title="Register", form=form)

        max_id = db.session.query(func.max(User.id)).scalar() or 0

        default_role = Role.query.filter_by(id=1).first()
        if not default_role:
            flash("Default role with ID 1 is not found in the database.", "error")
            return render_template("register.html", title="Register", form=form)

        # Új User létrehozása
        new_user = User(
            id=max_id + 1,
            name=form.name.data,
            email=form.email.data,
            password=form.password.data,
            phone=form.phone.data,
            address_id=1
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

#register blueprints here
from app.blueprints.user import bp as bp_user
bp.register_blueprint(bp_user, url_prefix='/user')

from app.blueprints.item import bp as bp_item
bp.register_blueprint(bp_item, url_prefix='/item')

from app.blueprints.order import bp as bp_order
bp.register_blueprint(bp_order, url_prefix='/order')

from app.blueprints.storekeeper import bp as bp_storekeeper
bp.register_blueprint(bp_storekeeper, url_prefix='/storekeeper')

from app.blueprints.courier import bp as bp_courier
bp.register_blueprint(bp_courier, url_prefix='/courier')

from app.blueprints.shipment import bp as bp_shipment
bp.register_blueprint(bp_shipment, url_prefix='/shipment')

from app.blueprints.supplier import bp as bp_supplier
bp.register_blueprint(bp_supplier, url_prefix='/supplier')

from app.models import *