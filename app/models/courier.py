from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from typing import List, Optional
from werkzeug.security import generate_password_hash, check_password_hash

class Courier(db.Model):
    __tablename__ = "couriers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[Optional[str]]
    phone: Mapped[str] = mapped_column(String(30))

    orders: Mapped[List["Order"]] = relationship(back_populates="courier", lazy=True)