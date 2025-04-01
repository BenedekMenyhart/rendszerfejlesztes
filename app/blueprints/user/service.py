from app.extensions import db
from app.blueprints.user.schemas import UserResponseSchema, RoleSchema
from app.models.user import User
from app.models.address import Address
from app.models.role import Role

from sqlalchemy import select


class UserService:

    @staticmethod
    def user_registrate(request):
        try:
            if db.session.execute(select(User).filter_by(email=request["email"])).scalar_one_or_none():
                return False, "E-mail already exist!"

            request["address"] = Address(**request["address"])
            user = User(**request)
            user.set_password(user.password)
            user.roles.append(
                db.session.execute(select(Role).filter_by(name="User")).scalar_one()
            )
            db.session.add(user)
            db.session.commit()
        except Exception as ex:
            return False, "Incorrect User data!"
        return True, UserResponseSchema().dump(user)

    @staticmethod
    def user_login(request):
        try:
            user = db.session.execute(select(User).filter_by(email=request["email"])).scalar_one()
            if not user.check_password(request["password"]):
                return False, "Incorrect e-mail or password!"
        except Exception as ex:
            return False, "Incorrect Login data!"
        return True, UserResponseSchema().dump(user)

    @staticmethod
    def user_list_roles():
        roles = db.session.query(Role).all()
        return True, RoleSchema().dump(obj=roles, many=True)

    @staticmethod
    def list_user_roles(uid):
        user = db.session.get(User, uid)
        if user is None:
            return False, "User not found!"
        return True, RoleSchema().dump(obj=user.roles, many=True)

    @staticmethod
    def user_add_address(request):
        try:
            address = Address(**request)
            db.session.add(address)
            db.session.commit()
        except Exception as ex:
            return False, "Incorrect Address data!"
        return True, address.id