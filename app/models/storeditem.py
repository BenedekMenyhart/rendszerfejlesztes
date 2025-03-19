from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db
from app.models.orderitem import OrderItem


class StoredItem(db.Model):
    __tablename__ = 'stored_items'
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    quantity_available: Mapped[int] = mapped_column(nullable=False)
    quantity_reserved: Mapped[int] = mapped_column(nullable=False)
    quantity_requested : Mapped[int] = mapped_column(nullable=False)

    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="stored_items")