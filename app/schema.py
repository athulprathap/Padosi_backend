# from pydantic import BaseModel, EmailStr
# from  datetime import datetime
# from typing import Optional
# from pydantic.types import conint

# # Post models
# class PostBase(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     created_at = datetime

# #The "createPost" class will automatically inherit the "PostBase" proprties and populate every field
# class CreatePost(PostBase): 
#     pass
# class UserOpt(BaseModel):  #(this only returns listed fields for User)
#     id: int
#     username: str
#     email: EmailStr
#     created_at = datetime 
#     class Config:
#         orm_mode = True
        
# class PostOpt(PostBase):  #(returns listed fields for Post)
#     id: int
#     published: bool
#     user_id : int
#     user : UserOpt
#     class Config:
#         orm_mode = True

# class PostAll(BaseModel):
#     Post: PostOpt
#     likes: int
#     class Config:
#         orm_mode = True

# # User models
# class UserBase(BaseModel):
#     username: str 
#     email: str
#     password: str
#     # image: str
#     created_at = datetime 

# class CreateUser(UserBase):
#      pass
# class UserAuth(BaseModel):
#     email: EmailStr
#     password: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     id: Optional[str] = None
    

# class Likes(BaseModel):
#     post_id: int
#     dir: conint(le=1)