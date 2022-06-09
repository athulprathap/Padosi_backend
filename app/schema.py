from pydantic import BaseModel
from datetime import datetime

# Post models
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    created_at = datetime

class CreatePost(PostBase): #The "createPost" class will automatically inherit the "PostBase" proprties and populate every field
    pass

#Return response (this only returns listed fields)
class PostOpt(BaseModel):
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
    created_at: datetime

class CreateUser(UserBase):
    pass

class UserOpt(BaseModel):
    username: str
    email: str