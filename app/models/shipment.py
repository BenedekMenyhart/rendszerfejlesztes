from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db



class Shipment(db.Model):
    __tablename__ = 'shipments'
    id: Mapped[int] = mapped_column(primary_key=True)

    expected_at: Mapped[int] = mapped_column(nullable=False)
    received: Mapped[bool] = mapped_column(nullable=False)

    items : Mapped[List["ShipmentItem"]] = relationship(back_populates="shipment")