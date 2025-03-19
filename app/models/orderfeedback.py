from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.order import Order

class OrderFeedback(db.Model):
    __tablename__ = 'order_feedbacks'
    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    order: Mapped["Order"] = relationship(back_populates="orders")

    content: Mapped[str] = mapped_column(String(256), nullable=False)
