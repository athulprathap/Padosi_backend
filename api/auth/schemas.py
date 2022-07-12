import email
from pydantic import BaseModel, Field


class UserList(BaseModel):
    email: str
    fullname: str


class UserCreate(UserList): # this class uses base model to define the fields
    password: str # password is a required field

class UserPassword(BaseModel):
    password: str

class UserPWD(UserList):
    password: str