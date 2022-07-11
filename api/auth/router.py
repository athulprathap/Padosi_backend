from sys import prefix
from urllib import response
from fastapi import APIRouter, Depends, HTTPException, status
from auth import schemas
from auth import crud
from utils import cryptoUtil

router = APIRouter(
    prefix = "/api/v1"
) # type: APIRouter

@router.post("/auth/register", response_model=schemas.UserList)  
async def register(user: schemas.UserCreate): # register a new user

    # check user exist
    result = await crud.find_existed_user(user.email)
    if result:
        raise HTTPException(status_code=400, detail="User already exist")
    
    # create new user
    # hash password here 
    user.password = cryptoUtil.get_password_hash(user.password)
    await crud.save_user(user)

    return {**user.dict(), "message": "User created successfully"}

