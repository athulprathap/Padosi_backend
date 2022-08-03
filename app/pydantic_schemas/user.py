from pydantic import BaseModel, EmailStr
from  datetime import datetime
from typing import Optional
from pydantic.types import conint


# User models
class User(BaseModel):
    username: str 
    email: str
    password: str
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
        
