from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.storeditem import StoredItem


class ShipmentItem(db.Model):
    __tablename__ = 'shipment_items'
    id: Mapped[int] = mapped_column(primary_key=True)

    stored_item_id: Mapped[int] = mapped_column(ForeignKey("stored_items.id"))
    stored_items : Mapped["StoredItem"] = relationship(back_populates="stored_items")

    qunatity : Mapped[int] = mapped_column(Integer, default = 0)
