from typing import List
from uuid import UUID, uuid4
from pydantic import EmailStr
from sqlalchemy import Column, String, Uuid, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.service import Base
from enum import Enum
from order.orderModel import Order
from product.productModel import Product

#That's the users role, that defines permissions following the RBAC principles.
class Role(Enum):
    BUYER = 'BUYER'
    SELLER = 'SELLER'

class User(Base):
    __tablename__="User"
    id: Mapped[UUID] = mapped_column(
        primary_key=True, 
        default=uuid4
    )
    nickname: Mapped[str]
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    role: Mapped[Role]
    earnings: Mapped[float] = mapped_column(default=0.0)
    Product: Mapped[List["Product"]] = relationship(back_populates="User")
    Order: Mapped[List["Order"]] = relationship(back_populates="User")
