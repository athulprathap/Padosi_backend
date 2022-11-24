from pydantic import BaseModel, EmailStr, constr
from  datetime import datetime
from typing import Dict, Optional, List
from pydantic import BaseModel, Field
from pydantic.types import conint
from typing import List
from datetime import date

# User models
class User(BaseModel):
    username: str 
    email: str
    password: constr(min_length=6, max_length=30)
    # image: str
    created_at = datetime 


class CreateUser(User):
     pass
 
class admin(BaseModel):
    username: str 
    email: str
    password: constr(min_length=6, max_length=30)
    # image: str
    created_at = datetime 
    is_admin = str

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

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    created_at = datetime

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

class CreateComment(BaseModel):
    post_id: int
    content: str

class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    user_id: int
    post_id: int
    com_owner: Optional[UserBase]  # NOTE: use optional just for testing

    class Config:
        orm_mode = True

    class config:
        orm_mode = True

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

class EmailSchema(BaseModel):
   email: List[EmailStr]

class VerifyOTP(CreateOTP):
    session_id: str
    otp_code: str


class InfoOTP(VerifyOTP):
    otp_failed_count: int
    status: str

class address(BaseModel):
    housenumber: str
    apartment: str
    city: str
    area: str
    pincode: int
    state: str
    class Config:
        orm_mode = True
class addressCreate(address):
    pass

class UserEdit(address):
    id: int

    class Config:
        orm_mode = True

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

class BlockedUser(BaseModel):
    is_blocked:str

class ReportUser(BaseModel):
    user_id: int
    message: str
    # viewed: bool

class Reportpost(BaseModel):
    message: str
    post_id: int
    count:int
    # viewed: bool
    
class DeviceToken(BaseModel):
    token: str

class Events(BaseModel):
    content: str
    description: str
    area: str
    region: str
    pincode: int

class EventRespond(BaseModel):
    event_id: int
    dir: int

class UserCreate(BaseModel):
    email: EmailStr

class SetPassword(BaseModel):
    email:EmailStr
    passcode:str
    password: str

class UserDevice(BaseModel):
    id: int
    user_id: int
    token: str
    device_info: Optional[Dict]


class UserDevicePayload(BaseModel):
    user_id: int = Field(..., gt=0, description="user_id must be greater than 0")
    token: str
    device_info: Optional[Dict]


class ErrorResponse(BaseModel):
    count: int = 0
    errors: Optional[List[Dict]]


class Response(BaseModel):
    success_count: int
    message: str
    error: ErrorResponse


class MessagePayload(BaseModel):
    user_id: int = Field(..., gt=0, description="user_id must be greater than 0")
    message: str
    notify: Dict


    # urgent_alert models
class urgent_alerts(BaseModel):
    title: str
    content: str
    published: bool = True
    created_at = datetime

#The "createalert" class will automatically inherit the "Base" proprties and populate every field
class Createalert(urgent_alerts): 
    pass

class Search(BaseModel):
    recent_search:str
    class Config():
        orm_mode=True

class ChangeAddress(BaseModel):
    message:str
    channge_city: str
    chnage_area: str

class AdminPermission(BaseModel):
    allowance: str

class polls(BaseModel):
    content: str
    option1: str
    option2: str

class Addpolls(polls):
    option3: Optional[str]
    option4: Optional[str]
    option5: Optional[str]
    option6: Optional[str]

class UserProfileTwo(BaseModel):
    sex: Optional[str]
    date_of_birth: Optional[date]

class UserProfileOne(BaseModel):
    mobile: Optional[str]
    # is_verified: Optional[bool]

class UserProfile(UserProfileOne, UserProfileTwo):
    full_name: str

class Mobile(BaseModel):
    mobile: str

class OtpVerify(BaseModel):
    otp:str

class PostImage(Post):
    image: str