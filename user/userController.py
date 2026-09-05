from fastapi import APIRouter, Depends, HTTPException, status
from auth.auth import TokenPayload, create_token, verify_token
from user.userDTO import UserDTO, UserRegisterResponse
from user.userModel import User
from database.service import session
import bcrypt
from user.userModel import Role
from sqlalchemy import select


router = APIRouter(
    prefix = '/users',
    tags=["User"]
)

@router.post("/", status_code=201, response_model=UserRegisterResponse)
async def signup(dto: UserDTO):
    if not dto.nickname or not dto.email or not dto.name or not dto.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All the fields are required!"
        )
    existsBase = select(User).where(User.nickname == dto.nickname or User.email == dto.email or User.name == dto.name)
    with session() as s: 
        try: 
            exists = s.execute(existsBase) #Verify if user exists
            if exists: 
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User already exists!"
                )
            role = Role(Role.BUYER)
            if dto.role.upper() == 'SELLER':
                role = Role(Role.SELLER)
            hash_password = bcrypt.hashpw(dto.password.encode("utf-8"), bcrypt.gensalt(10))
            new_user = User(nickname=dto.nickname, email=dto.email, name=dto.name, password=hash_password, role=role)
            s.add(new_user)
            s.commit()
            s.refresh(new_user)
            return new_user
        except Exception:
            raise Exception()

@router.post('/login')
async def login(dto: UserDTO):
    if not dto.nickname or not dto.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All the fields are required!"
        )
    existsBase = select(User).where(User.nickname == dto.nickname)
    with session() as s:
        exists = s.execute(existsBase).scalar_one_or_none()
        if not exists:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!"
        )
        correctPassword = bcrypt.checkpw(dto.password.encode("utf-8"), exists.password.encode("utf-8"))
        if not correctPassword:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Incorrect password!"
            )
        token = create_token({"sub": exists.nickname})
        return { "token": token }

@router.patch('/', response_model=UserRegisterResponse)
async def change_profile(dto: UserRegisterResponse, user: TokenPayload = Depends(verify_token)):
    userBase = select(User).where(User.id == user.id)
    nickBase = select(User).where(User.nickname == user.nickname)
    with session() as s:
        userAuth = s.execute(userBase).scalar_one_or_none()
        nickExists = s.execute(nickBase).scalar_one_or_none()
        if not userAuth:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You must")
        
        userAuth.nickname = dto.nickname 
        userAuth.email = dto.email
        userAuth.name = dto.name
        userAuth.role = Role(dto.role.upper())
        s.commit()
        s.refresh(userAuth)
        return userAuth

@router.patch('/delete')
def delete_user(user: TokenPayload = Depends(verify_token)):
    userBase = select(User).where(User.id == user.id)
    with session() as s:
        userAuth = s.execute(userBase).scalar_one_or_none()
        if not userAuth:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="You aren't authenticated!"
            )
        userAuth.nickname = f"inative_user_{user.id}"
        userAuth.email = f"removed_user_{user.id}@inativeemail.com"
        userAuth.name = f"Inative User {user.id}"
        userAuth.password = "INVALID_PASSWORD"
