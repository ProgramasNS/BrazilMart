from typing import Optional
from pydantic import BaseModel, EmailStr
#There is two options of login: if the nickname, login with nickname; if the e-mail, login with e-mail. If both, with both.
class UserDTO(BaseModel):
    nickname: Optional[str]
    email: Optional[str]
    name: Optional[str]
    role: str
    password: str

#That's the response (and generic model to update users)
class UserRegisterResponse(BaseModel):
    nickname: str
    email: str 
    name: str
    role: str
