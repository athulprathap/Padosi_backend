from pydantic import BaseModel, EmailStr
from  datetime import datetime
from typing import Optional
from pydantic.types import conint
from .user import UserOpt



# urgent_alert models
class urgent_alerts(BaseModel):
    title: str
    content: str
    published: bool = True
    created_at = datetime

#The "createalert" class will automatically inherit the "Base" proprties and populate every field
class Createalert(urgent_alerts): 
    pass

"""
class UserOpt(BaseModel):  #(this only returns listed fields for User)
    id: int
    username: str
    email: EmailStr
    created_at = datetime 
    class Config:
        orm_mode = True
        
class PostOpt(urgent_alerts):  #(returns listed fields for Post)
    id: int
    published: bool
    user_id : int
    user : UserOpt
    class Config:
        orm_mode = True

class PostAll(BaseModel):
    Post: PostOpt
    likes: int
    class Config:
        orm_mode = True

class Likes(BaseModel):
    post_id: int
    dir: conint(le=1)
    
    """