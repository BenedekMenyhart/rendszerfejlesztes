from typing import List

from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db, Base
#from app.models.order import Order
from app.models.storeditem import StoredItem
from app.models.shipment import Shipment

OrderItemsShipments = Table(
    "order_items_shipments",
    Base.metadata,
    Column("order_item_id", ForeignKey("order_items.id")),
    Column("shipment_id", ForeignKey("shipments.id"))
)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    order: Mapped["Order"] = relationship(back_populates="orders")

    stored_item_id: Mapped[int] = mapped_column(ForeignKey("stored_items.id"))
    stored_item: Mapped["StoredItem"] = relationship(back_populates="orders")

    quantity: Mapped[int] = mapped_column(nullable=False)

    shipment: Mapped[List["Shipment"]] = relationship(back_populates="shipments", secondary=OrderItemsShipments)