from datetime import datetime
import email
from typing import Optional
from pydantic import BaseModel, Field


class UserList(BaseModel):
    id: int = None
    email: str
    fullname: str
    created_on : Optional[datetime] = None
    status: str = None

class UserCreate(BaseModel):
    email: str = Field(..., example="sjdecode@gmail.com")
    password: str = Field(..., example="sjdecode")
    fullname: str = Field(..., example="Neng Channa")
    

class UserPassword(BaseModel):
    password: str

class ForgotPassword(BaseModel):
    email: str

class EmailRequest(BaseModel):
    email: str

class ResetPassword(BaseModel):
    new_password: str
    confirm_password: str
