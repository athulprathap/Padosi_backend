from pydantic import BaseModel, EmailStr
from  datetime import datetime
from typing import Optional
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    created_at = datetime

class CreatePost(PostBase): 
    pass
class UserOpt(BaseModel): 
    id: int
    username: str
    email: EmailStr
    created_at = datetime 
    class Config:
        orm_mode = True
        
class PostOpt(PostBase):  
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


class UserBase(BaseModel):
    username: str 
    email: str
    password: str
    # image: str
    created_at = datetime 

class CreateUser(UserBase):
     pass
class UserAuth(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    

class Likes(BaseModel):
    post_id: int
    dir: conint(le=1)

class UserList(BaseModel):
    id: int = None
    email: str
    fullname: str
    created_on : Optional[datetime] = None
    status: str = None

class CreateOTP(BaseModel):
    recipient_id: str


class VerifyOTP(CreateOTP):
    session_id: str
    otp_code: str


class InfoOTP(VerifyOTP):
    otp_failed_count: int
    status: str

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

class DeviceToken(BaseModel):
    token: str