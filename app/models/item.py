from __future__ import annotations

from app.extensions import db
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String


class Item(db.Model):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[int]
    quantity_available: Mapped[int]=mapped_column(nullable=False)

    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="item")

    deleted: Mapped[int] = mapped_column(default=0)