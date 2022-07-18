from sys import prefix
from fastapi import APIRouter, Depends, HTTPException, status
from api.auth import schemas as auth_schemas
from api.users import schemas as users_schemas
from api.utils import constantUtil, jwtUtil
from api.users import crud

router = APIRouter(
    prefix="/api/v1"
)

@router.get("/user/profile")
async def get_user_profile(current_user: auth_schemas.UserList= Depends(jwtUtil.get_current_user)):
    return current_user

@router.patch("/user/profile")
async def update_user_profile(
    request: users_schemas.UserUpdate,
    current_user: auth_schemas.UserList= Depends(jwtUtil.get_current_user)):

    # update user profile
    await crud.update_user(request, current_user)

    return {
        "status_code" : status.HTTP_200_OK,
        "message" : "User profile updated successfully"
    }

@router.delete("/user/profile")
async def deactivate_account(
    current_user: auth_schemas.UserList= Depends(jwtUtil.get_current_user)):

    # deactivate user account
    await crud.deactivate_user(current_user)

    return {
        "status_code" : status.HTTP_200_OK,
        "message" : "User account deactivated successfully"
    }
