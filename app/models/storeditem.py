from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app import db


class StoredItem(db.Model):
    tablename = 'stored_items'
    id: Mapped[int] = mapped_column(primary_key=True)


    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    quantity_available: Mapped[int] = mapped_column(nullable=False)
    quantity_reserved: Mapped[int] = mapped_column(nullable=False)
    quantity_requested : Mapped[int] = mapped_column(nullable=False)