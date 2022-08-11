from pydantic import BaseModel, EmailStr, constr
from  datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic.types import conint


# User models
class User(BaseModel):
    username: str 
    email: str
    password: constr(min_length=6, max_length=30)
    # image: str
    created_at = datetime 


class CreateUser(User):
     pass
 

class UserOpt(BaseModel):  #(this only returns listed fields for User)
    id: int
    username: str
    email: EmailStr
    created_at = datetime 
    class Config:
        orm_mode = True
        
class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    
    class Config:
        orm_mode = True
        
class updatePassword(BaseModel):
    password: constr(min_length=7, max_length=100)
    salt: str

    class Config:
        orm_mode = True
