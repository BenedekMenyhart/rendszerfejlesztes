from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.supplier import Supplier


class Shipment(db.Model):
    tablename = 'shipments'
    id: Mapped[int] = mapped_column(primary_key=True)

    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))
    supplier: Mapped["Supplier"] = relationship(back_populates="suppliers")

    expected_at: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    received: Mapped[bool] = mapped_column(nullable=False)