from time import clock_settime
from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional
from api.enums import post as post_enum
from api.auth import schemas as auth_schemas

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int 
    owner: Optional[str] = auth_schemas.UserList
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Hello World",
                "content": "This is my first post",
                "published": True
            }
        }
