import email
from pydantic import BaseModel, Field


class UserList(BaseModel):
    email: str
    fullname: str


class UserCreate(BaseModel):
    email: str = Field(..., example="sjdecode@gmail.com")
    password: str = Field(..., example="sjdecode")
    fullname: str = Field(..., example="Neng Channa")

class UserPassword(BaseModel):
    password: str

class UserPWD(UserList):
    password: str