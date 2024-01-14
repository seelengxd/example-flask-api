from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import db

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    hashed_password: Mapped[str]

    todos: Mapped[List["Todo"]] = relationship(back_populates="user")