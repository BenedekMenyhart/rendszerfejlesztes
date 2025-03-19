from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db


class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(64), nullable=False)

