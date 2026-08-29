from uuid import UUID, uuid4
from pydantic import EmailStr
from sqlalchemy import Column, ForeignKey, String, Uuid, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.service import Base
from datetime import date
from user.userModel import User

class Product(Base):
    __tablename__="Product"
    id: Mapped[UUID] = mapped_column(
            primary_key=True, 
            default=uuid4
    )
    postDate: Mapped[date] = mapped_column(default=date.today)
    updateDate: Mapped[date] = mapped_column(default=date.today)
    price: Mapped[float]
    name: Mapped[str]
    creatorId: Mapped[UUID] = mapped_column(ForeignKey("User.id"))
    User: Mapped["User"] = relationship(back_populates="Product")
    