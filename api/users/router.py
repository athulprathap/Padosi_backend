from sys import prefix
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from api.auth import schemas as auth_schemas
from api.users import schemas as users_schemas
from api.utils import constantUtil, jwtUtil
from api.users import crud as user_crud
from api.auth import crud as auth_crud
import os


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
    await user_crud.update_user(request, current_user)

    return {
        "status_code" : status.HTTP_200_OK,
        "message" : "User profile updated successfully"
    }

@router.delete("/user/profile")
async def deactivate_account(
    current_user: auth_schemas.UserList= Depends(jwtUtil.get_current_user)):

    # deactivate user account
    await user_crud.deactivate_user(current_user)

    return {
        "status_code" : status.HTTP_200_OK,
        "message" : "User account deactivated successfully"
    }


@router.get("/user/logout")
async def logout(
        token: str = Depends(jwtUtil.get_token_user),
        currentUser: auth_schemas.UserList = Depends(jwtUtil.get_current_active_user)
):
    await user_crud.save_black_list(token, currentUser)
    return {"message": "you logged out successfully"}

# make a api to upload user profile images
@router.patch("/user/upload-profile-image")
async def upload_profile_image(
    file: UploadFile = File(...),
    currentUser: auth_schemas.UserList = Depends(jwtUtil.get_current_active_user)
):
    try:
        cwd = os.getcwd()
        path_image_dir = "upload-images/user/profile/"+str(currentUser.id) + "/"
        full_image_path = os.path.join(cwd, path_image_dir, file.filename)

        # Create directory if not exist
        if not os.path.exists(path_image_dir):
            os.mkdir(path_image_dir)

        # Rename file
        file_name = full_image_path.replace(file.filename, "profile.png")

        # Write file
        with open(file_name, 'wb+') as f:
            f.write(file.file.read())
            f.flush()
            f.close()

        return {"profile_image": os.path.join(path_image_dir, "profile.png")}

    except Exception as e:
        print(e)

