from __future__ import annotations

from typing import List, Optional
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Integer

from app.models.order import Order
from app.models.user import User



class Address(db.Model):
    __tablename__ = "addresses"
    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(30))
    street: Mapped[str] = mapped_column(String(30))
    postalcode: Mapped[int]

    user: Mapped["User"] = relationship(back_populates="address")
    orders: Mapped[List["Order"]] = relationship(back_populates="address")
