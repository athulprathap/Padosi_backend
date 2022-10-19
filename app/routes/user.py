from fastapi import FastAPI, Response, requests, status, HTTPException, Depends, APIRouter, File, UploadFile
from sqlalchemy.orm import Session
from .. import oauth2
from .. import model,schema
from sqlalchemy import func
from ..database import get_db
from ..modules.users.userRepository import register_new, singleUser, updateUser
from ..pydantic_schemas.user import CreateUser, UserOpt,  User, UserUpdate
import os


router = APIRouter( tags = ['Users'])


@router.post("/Register", status_code=status.HTTP_201_CREATED, response_model=UserOpt)
async def register(user:User, db:Session = Depends(get_db)):
    return register_new(db=db, user=user)


@router.get("/users/{id}", response_model=UserOpt)
async def get_user(id:int, db: Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):
    user = singleUser(id=id, db=db)
    if user is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found!")
    return user


@router.put("/users/{id}", response_model=UserOpt)
async def editUser(id:int, user: UserUpdate , db:Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):
    my_update = updateUser(id=id, user=user, db=db, values=dict(user))
    if my_update is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= "You can't perform this action!!")
    return my_update

@router.get("/nearby_users/{user_id}")
def find_nearby_users(user_id: int, radius: int = 10, db: Session = Depends(get_db)):
    """raius is in km"""
    current_user = db.query(model.Address).filter(model.Address == user_id).first()
    users = db.query(model.Address).filter(model.Address.user_id != user_id, func.public.calculate_distance(model.Address.latitude, model.Address.longitude, current_user.latitude, current_user.longitude, "K") <= radius).all()
    return users

@router.patch("/user/upload-profile-image")
async def upload_profile_image(
    file: UploadFile = File(...),
    currentUser: schema.UserList = Depends(oauth2.get_current_active_user)
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

@router.delete("/user/profile")
async def deactivate_account(
    current_user: schema.UserList= Depends(oauth2.get_current_user)):

    # deactivate user account
    await model.deactivate_user(current_user)

    return {
        "status_code" : status.HTTP_200_OK,
        "message" : "User account deactivated successfully"
    }
