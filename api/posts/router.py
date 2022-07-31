from sys import prefix
from turtle import pos
from urllib import response
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from api.auth import schemas as auth_schemas
from api.posts import schemas as posts_schemas
from api.utils import constantUtil, jwtUtil
from api.users import crud as user_crud
from api.auth import crud as auth_crud
from api.posts import crud as post_crud
from api.enums import post as post_enum
import os

router = APIRouter(
    prefix="/api/v1"
)

@router.post("create-post",response_model= posts_schemas.Post)
async def create_post(post: posts_schemas.PostCreate,
            currentUser: auth_schemas.UserList = Depends(jwtUtil.get_current_active_user)):
    print(currentUser)


    # create a new post in the database
    post_id = post_crud.create_post(request=post, currentUser=currentUser)
    return {
        "Okay": "Post created"
    }
