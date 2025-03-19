import enum
from typing import List

from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db, Base
from app.models.customer import Customer
#from app.models.courier import Courier
from app.models.orderfeedback import OrderFeedback
from app.models.orderitem import OrderItem

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
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True)

    status : Mapped[Statuses] = mapped_column()

    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    customer: Mapped["Customer"] = relationship(back_populates="customers")

    courier: Mapped[List["Courier"]] = relationship(back_populates="couriers", secondary=OrdersCouriers)

    items: Mapped[List["OrderItem"]] = relationship(back_populates="orders")

    feedback: Mapped["OrderFeedback"] = relationship(back_populates="orders")

    created_at: Mapped[str] = mapped_column(String(64), nullable=False)

