from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class Order(db.Model):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="users")

    phone: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable=False)

    locality: Mapped[str] = mapped_column(String(64), nullable=False)  # város vagy falu neve
    zip_code: Mapped[str] = mapped_column(String(64), nullable=False)
    address: Mapped[str] = mapped_column(String(64), nullable=False)
