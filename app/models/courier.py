from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.user import User
from app.models.order import Order

class Courier(db.Model):
    __tablename__ = 'couriers'
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="users")

    orders: Mapped[list["Order"]] = relationship(back_populates="couriers")