from pydantic import BaseModel, EmailStr
from datetime import datetime

# Post models
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    created_at = datetime

#The "createPost" class will automatically inherit the "PostBase" proprties and populate every field
class CreatePost(PostBase): 
    pass


class PostOpt(BaseModel):  #(returns listed fields for Post)
    id: int
    title: str
    content: str
    published: bool
    class Config:
        orm_mode = True


# User models
class UserBase(BaseModel):
    username: str
    email: str
    password: str
    created_at = datetime 

class CreateUser(UserBase):
     pass

class UserOpt(BaseModel):  #(this only returns listed fields for User)
    id: int
    username: str
    email: EmailStr
    class Config:
        orm_mode = True

class UserAuth(BaseModel):
    email: EmailStr
    password: str