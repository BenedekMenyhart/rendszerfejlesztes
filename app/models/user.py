from app.extensions import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from sqlalchemy import ForeignKey, Column, Table
from typing import List, Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Szerepkörök kapcsolótáblája
UserRole = Table(
    "userroles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("role_id", ForeignKey("roles.id"))
)

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[Optional[str]]
    password: Mapped[str] = mapped_column(String(30))

    # Egyedi courier_id mező – ez nem kapcsolat, csak érték
    courier_id: Mapped[Optional[int]] = mapped_column(nullable=True)

    # Szerepek kapcsolata (sok-sok)
    roles: Mapped[List["Role"]] = relationship(
        secondary=UserRole,
        back_populates="users"
    )

    # Cím és telefonszám kapcsolatok
    address_id: Mapped[Optional[int]] = mapped_column(ForeignKey("addresses.id"))
    address: Mapped["Address"] = relationship(back_populates="user", lazy=True)

    phonenumber_id: Mapped[Optional[int]] = mapped_column(ForeignKey("phonenumbers.id"))
    phonenumber: Mapped["Phonenumber"] = relationship(back_populates="user", lazy=True)

    # Felhasználó által leadott rendelések (user_id alapján)
    orders: Mapped[List["Order"]] = relationship(
        back_populates="user",
        foreign_keys="Order.user_id",
        lazy=True
    )

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, name={self.name!s}, email={self.email!r}, "
            f"courier_id={self.courier_id!r})"
        )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
