from uuid import UUID

from fastapi import APIRouter
from sqlalchemy import select

from product.productModel import Product
from database.service import session


router = APIRouter(
    prefix="orders",
    tags=["order"]
)
#Any authenticated people can create orders, being or not buyers
@router.post('/{id}')
def create_order(id: UUID):
    productBase = select(Product).where(Product.id == id)
    with session() as s:
        product = s.execute(productBase)
        
