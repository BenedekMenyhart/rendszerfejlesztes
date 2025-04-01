import enum
from typing import List,Optional

from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db, Base



class Statuses(enum.Enum):
    Received = "received"
    Processing = "processing"
    Processed = "processed"
    AssignedToCourier = "assigned_to_courier"
    DeliveryStarted = "delivery_started"
    Delivered = "delivered"
    ReceptionConfirmed = "reception_confirmed"



class Order(db.Model):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    user: Mapped[Optional["User"]] = relationship(back_populates="orders")

    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    address: Mapped["Address"] = relationship(back_populates="orders")


    created_at: Mapped[str] = mapped_column(String(64), nullable=False)


    status: Mapped[Statuses] = mapped_column()
    feedback: Mapped[Optional[str]] = mapped_column(nullable=True)
    items: Mapped[List["OrderItem"]] = relationship(back_populates="orders")

