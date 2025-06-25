from __future__ import annotations
from typing import List
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String



class Phonenumber(db.Model):
    __tablename__ = "phonenumbers"
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(30))

    user: Mapped["User"] = relationship(back_populates="phonenumber")
    orders: Mapped[List["Order"]] = relationship(back_populates="phonenumber")#buyer's
