from pydantic import BaseModel, EmailStr
from typing import Optional

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
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str]
