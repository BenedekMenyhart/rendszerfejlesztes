import enum
from typing import List,Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db



class Statuses(enum.Enum):
    Received = "Received"
    Processing = "Processing"
    Processed = "Processed"
    AssignedToCourier = "AssignedToCourier"
    DeliveryStarted = "DeliveryStarted"
    Delivered = "Delivered"
    ReceptionConfirmed = "ReceptionConfirmed"

    @classmethod
    def missing(cls, value):
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        raise LookupError(
            f"'{value}' is not among the defined enum values. Enum name: {cls.name}. Possible values: {', '.join([m.value for m in cls])}.")


class Order(db.Model):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    user: Mapped[Optional["User"]] = relationship(back_populates="orders")

    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    address: Mapped["Address"] = relationship(back_populates="orders")


    created_at: Mapped[str] = mapped_column(String(64), nullable=False)

    courier_id: Mapped[Optional[int]] = mapped_column(ForeignKey("couriers.id"))
    courier: Mapped[Optional["Courier"]] = relationship(back_populates="orders")

    status: Mapped[Statuses] = mapped_column()
    feedback: Mapped[Optional[str]] = mapped_column(nullable=True)

    items: Mapped[List["OrderItem"]] = relationship(back_populates="order")