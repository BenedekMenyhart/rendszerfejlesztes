from __future__ import annotations

from typing import List
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String



class Address(db.Model):
    __tablename__ = "addresses"
    id: Mapped[int] = mapped_column(primary_key=True)
    postalcode: Mapped[int]
    city: Mapped[str] = mapped_column(String(30))
    street: Mapped[str] = mapped_column(String(30))


    user: Mapped["User"] = relationship(back_populates="address")
    orders: Mapped[List["Order"]] = relationship(back_populates="address")
