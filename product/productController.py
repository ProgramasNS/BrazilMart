from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from auth.auth import TokenPayload, verify_token
from product.productDTO import ProductDTO
from database.service import session
from product.productModel import Product
from user.userModel import User

router = APIRouter(
    prefix='products',
    tags=['product']
)

@router.post('/', status_code=201, response_model=ProductDTO)
async def create_product(dto: ProductDTO, user: TokenPayload = Depends(verify_token)):
    if not user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You aren't authenticated!")
    if user.role != "SELLER":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only sellers can create new products!")
    if not dto.name or not dto.price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All the fields are required and the price can't be null!")
    with session() as s:
        new_product = Product(name=dto.name, price=dto.price, creatorId=user.id)
        s.add(new_product)
        s.commit()
        s.refresh(new_product)
        return new_product

@router.get('/')
async def get_products():
   productsBase = select(Product)
   with session() as s:
    return s.execute(productsBase).fetchall()

@router.get('/{id}')
async def get_products_by_seller(id: int):
   productsBase = select(Product).where(Product.creatorId == id)
   with session() as s:
    return s.execute(productsBase).fetchall()

@router.patch('/{id}')
async def update_product(dto: ProductDTO, id: int, user: TokenPayload = Depends(verify_token)):
   productBase = select(Product).where(Product.id == id)
   with session() as s:
    product = s.execute(productBase).scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found!"
        )
    if not user:
       raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="You aren't authenticated!"
       )
    if user.id != product.creatorId:
       raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN,
          detail = "Only the creator can edit the product!"
       )
    if dto.name:
       product.name = dto.name
    if dto.price:
       product.price = dto.price
    s.commit()
    s.refresh(product)
    return product

@router.delete('/{id}')
async def delete_product(id: int, user: TokenPayload = Depends(verify_token)):
   productBase = select(Product).where(Product.id == id)
   with session() as s:
    product = s.execute(productBase).scalar_one_or_none()
    if not product:
       raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail="Product not found!"
       )
    if not user:
       raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED
       )
    if product.creatorId != user.id:
       raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN,
          detail="Only the creator can delete products!"
       )
    s.delete(product)
    s.commit()