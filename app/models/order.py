import enum
from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from app.models.customer import Customer
from app.models.courier import Courier
from app.models.orderitem import OrderItem

class Statuses(enum.Enum):
    Received = "received"
    Processing = "processing"
    Processed = "processed"
    AssignedToCourier = "assigned_to_courier"
    DeliveryStarted = "delivery_started"
    Delivered = "delivered"
    RecipientConfirmed = "recipient_confirmed"


class Order(db.Model):
    tablename = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True)

    status : Mapped[Statuses] = mapped_column()

    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    customer: Mapped["Customer"] = relationship(back_populates="customers")

    courier_id: Mapped[int] = mapped_column(ForeignKey("couriers.id"))
    courier: Mapped["Courier"] = relationship(back_populates="couriers")

    items: Mapped[List["OrderItem"]] = relationship(back_populates="orders")

    created_at: Mapped[str] = mapped_column(String(64), nullable=False)

