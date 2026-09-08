from pydantic import BaseModel
from sqlalchemy import UUID
from user.userDTO import UserRegisterResponse
from user.userModel import User

class ProductDTO(BaseModel):
    name: str
    price: float

class ProductResponseDTO:
    name: str
    price: float
    creatorId: UUID
    creator: UserRegisterResponse