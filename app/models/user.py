from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db


class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(64), nullable=False)

    customer: Mapped[int] = relationship(back_populates="users")
    storekeeper: Mapped[int] = relationship(back_populates="users")
    supplier: Mapped[int] = relationship(back_populates="users")