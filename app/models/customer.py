from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
#from app.models.order import Order
from app.models.user import User


class Customer(db.Model):
    __tablename__ = 'customers'
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="users")

    phone: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable=False)

    locality: Mapped[str] = mapped_column(String(64), nullable=False) #város vagy falu neve
    zip_code: Mapped[str] = mapped_column(String(64), nullable=False)
    address: Mapped[str] = mapped_column(String(64), nullable=False)

    orders: Mapped[list["Order"]] = relationship(back_populates="customers")