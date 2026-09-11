from enum import Enum
from uuid import UUID, uuid4
from product.productModel import Product
from sqlalchemy import ForeignKey
from database.service import Base
from sqlalchemy.orm import Mapped, mapped_column
from user.userModel import User

class Status(Enum):
    
    WAITING_PAYMENT = "WAITING PAYMENT"
    PAID = "PAID"
    RECUSED = "RECUSED"
    
class Order(Base):
    __tablename__="Order"
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4
    )
    status: Mapped[Status] = mapped_column(default=Status(Status.WAITING_PAYMENT))
    productId = mapped_column(ForeignKey("Product.id"))
    Product: Mapped[Product]
    userId = mapped_column(ForeignKey("User.id"))
    User: Mapped[User]