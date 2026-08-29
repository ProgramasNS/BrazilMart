from fastapi import APIRouter, Depends, HTTPException, status
from auth.auth import TokenPayload, verify_token
from product.productDTO import ProductDTO
from database.service import session
from product.productModel import Product

router = APIRouter(
    prefix='products',
    tags=['product']
)

@router.post('/')
def create_product(dto: ProductDTO, user: TokenPayload = Depends(verify_token)):
    if not user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You aren't authenticated!")
    if user.role != "SELLER":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only sellers can create new products!")
    if not dto.name or not dto.price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All the fields are required and the price can't be null!")
    with session() as s:
      try:
        s.add(Product(name=dto.name, price=dto.price, creatorId=user.id))
        s.commit()
      except Exception as err:
        s.rollback()
        print(f'Error: {err}')
        return {'message': 'Something went wrong'}
      
