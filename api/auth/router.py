from os import access
from sys import prefix
from urllib import response
from fastapi import APIRouter, Depends, HTTPException, status
from api.auth import schemas
from api.auth import crud
from api.utils import cryptoUtil, constantUtil, jwtUtil
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix = "/api/v1"
) # type: APIRouter


# register router for /api/v1/auth/register

@router.post("/auth/register")  
async def register(user: schemas.UserCreate):

    # check user exist
    result = await crud.find_existed_user(user.email)
    if result:
        raise HTTPException(status_code=400, detail="User already exist")
    
    # create new user
    # hash password here 
    user.password = cryptoUtil.get_password_hash(user.password)
    await crud.save_user(user)

    return {**user.dict(), "message": "User created successfully"}


@router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    # check user exist
    result = await crud.find_existed_user(form_data.username)
    if not result:
        raise HTTPException(status_code=400, detail="User not found")
    
    # verify password
    user = schemas.UserCreate(**result)
    verified_password = cryptoUtil.verify_password(form_data.password, user.password)
    if not verified_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # create token 
    access_token_expires = jwtUtil.timedelta(minutes=constantUtil.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await jwtUtil.create_accces_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"

    }