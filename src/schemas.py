from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]
    username: Optional[str]



class Token(BaseModel):
    token : str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str]


class blockedToken(BaseModel):
    jwt_token : str

class blockedTokenData(blockedToken):
    id: Optional[int]
    created_at: datetime

class blockedTokenCreate(blockedToken):
    jwt_token: str