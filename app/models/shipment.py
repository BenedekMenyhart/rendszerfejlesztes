from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db



class Shipment(db.Model):
    __tablename__ = 'shipments'
    id: Mapped[int] = mapped_column(primary_key=True)

    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))
    supplier: Mapped["Supplier"] = relationship(back_populates="suppliers")

    expected_at: Mapped[str] = mapped_column(String(64), nullable=False)
    received: Mapped[bool] = mapped_column(nullable=False)