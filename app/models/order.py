import enum
from typing import List, Optional
from sqlalchemy import String, ForeignKey, Integer
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
    price: Mapped[Optional[int]] = mapped_column(nullable=True)
    deleted: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=False)

    # FELHASZNÁLÓ – idegen kulcsos kapcsolat
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    user: Mapped[Optional["User"]] = relationship(
        back_populates="orders",
        foreign_keys=[user_id]
    )

    # FUTÁR – csak sima integer mező, nem FK
    courier_id: Mapped[Optional[int]] = mapped_column(nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)

    phonenumber_id: Mapped[int] = mapped_column(ForeignKey("phonenumbers.id"))
    phonenumber: Mapped["Phonenumber"] = relationship(back_populates="orders")

    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    address: Mapped["Address"] = relationship(back_populates="orders")

    created_at: Mapped[str] = mapped_column(String(64), nullable=False)

    status: Mapped[Statuses] = mapped_column()
    feedback: Mapped[Optional[str]] = mapped_column(nullable=True)



    items: Mapped[List["OrderItem"]] = relationship(back_populates="order")
