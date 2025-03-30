import enum
from typing import List,Optional

from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db, Base
from app.models.address import Address
from app.models.orderfeedback import OrderFeedback
from app.models.orderitem import OrderItem
from app.models.user import User


class Statuses(enum.Enum):
    Received = "received"
    Processing = "processing"
    Processed = "processed"
    AssignedToCourier = "assigned_to_courier"
    DeliveryStarted = "delivery_started"
    Delivered = "delivered"
    RecipientConfirmed = "recipient_confirmed"

OrdersCouriers = Table(
    "orders_couriers",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id")),
    Column("courier_id", ForeignKey("couriers.id"))
)


class Order(db.Model):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    user: Mapped[Optional["User"]] = relationship(back_populates="orders")

    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    address: Mapped["Address"] = relationship(back_populates="orders")


    status: Mapped[Statuses] = mapped_column()
    feedback: Mapped[Optional[str]] = mapped_column(nullable=True)
    items: Mapped[List["OrderItem"]] = relationship(back_populates="orders")

