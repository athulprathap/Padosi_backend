from fastapi import FastAPI, Response, requests, status, HTTPException, Depends, APIRouter, File, UploadFile
from sqlalchemy.orm import Session
from  ..oauth2 import get_current_user,get_current_active_user
from app.api import model,schema,crud
from sqlalchemy import func
from typing import Optional, Dict
from ..database import get_db
from ..modules.userRepository import register_new, updateUser,singleUser
from ..schema import UserOpt,  User, UserUpdate
import os
from pyexpat import model
from .. import model, schema, utils, oauth2
from .. utils import send_otp_mail, random_with_N_digits, operation_after_block


router = APIRouter( tags = ['Users'])


@router.post("/Register", status_code=status.HTTP_201_CREATED, response_model=UserOpt)
async def register(user:User, db:Session = Depends(get_db)):
    return register_new(db=db, user=user)


@router.get("/users", response_model=UserOpt)
async def get_user(db: Session = Depends(get_db), account_owner: int = Depends(get_current_user)):
    user = db.query(model.User).filter(model.User.id == account_owner.id).first()
    if user is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found!")
    return user


@router.put("/users/{id}", response_model=UserOpt)
async def editUser(id, user: UserUpdate , db:Session = Depends(get_db), account_owner: int = Depends(get_current_user)):
    my_update = updateUser(id=id, user=user, db=db, values=dict(user))
    if my_update is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= "You can't perform this action!!")
    return my_update

@router.delete("/user/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id, db: Session = Depends(get_db), account_owner: int = Depends(get_current_user)):
    user=db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id {id} not found")
    user.delete(synchronize_session=False)
    db.commit()
    return "deleted successfully"

@router.get("/nearby_users/{user_id}")
def find_nearby_users(user_id: int, radius: int = 0, db: Session = Depends(get_db)):
    """raius is in km"""
    current_user = db.query(model.Address).filter(model.Address == user_id).first()
    users = db.query(model.Address).filter(model.Address.user_id != user_id, func.public.calculate_distance(model.Address.pincode, current_user.pincode, current_user.pincode, "K")<=radius).all()
    return users

@router.post("/adress/{user_id}")
def addres(event: schema.address, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    address = model.Address(user_id=current_user.id,housenumber=event.housenumber,apartment=event.apartment,
    city=event.city,area=event.area,pincode=event.pincode,state=event.state)

    db.add(address)
    db.commit()
    db.refresh(address)

    return address

@router.post("/change_adress/{user_id}")
def change_address(user: schema.ChangeAddress, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    address = model.ChangeAddress(user_id=current_user.id,change_city=user.channge_city,change_area=user.chnage_area,message=user.message)

    db.add(address)
    db.commit()
    db.refresh(address)

    return address

@router.patch("/user/upload-profile-image")
async def upload_profile_image(
    file: UploadFile = File(...),
    currentUser: schema.UserList = Depends(get_current_active_user)
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
    current_user: schema.UserList= Depends(get_current_user)):

    # deactivate user account
    await crud.deactivate_user(current_user)

    return {
        "status_code" : status.HTTP_200_OK,
        "message" : "User account deactivated successfully"
    }

@router.post("/report_user")
def report_user(report_user: schema.ReportUser, db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)):

    report = model.ReportUser(reported_to=report_user.user_id, reported_by=current_user.id, message=report_user.message)

    db.add(report)
    db.commit()
    db.refresh(report)
    
    if not report:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Please try again")

    return report

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schema.Events)
def update_address(id:int,add: schema.addressCreate, db: Session = Depends(get_db),values: Dict={}):
    permission = db.query(model.ChangeAddress).filter(model.ChangeAddress.user_id == id).first()
    value = permission.__getattribute__("allowance")
    
    change_address = db.query(model.Address).filter(
        model.Address.user_id == id)

    if not change_address.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {id} not found")
    
    # change_address.update({'housenumber' : add.housenumber, 'apartment': add.apartment, 'city': add.city, 'pincode': add.pincode, 'state': add.state})
    change_address.update(add)
    if value:
        db.commit()
        return change_address
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail=f"pls contact admin")



@router.post("/otp")
async def send_otp(userdata: schema.UserCreate, db: Session = Depends(get_db)):
    user_query = db.query(model.User).filter(model.User.email == userdata.email)
    # temp base set password 123456
    otp = str(random_with_N_digits(6))
    password = utils.hash(otp)
    status = send_otp_mail(userdata.email, otp)
    profile_exist = False
    user = user_query.first()
    if user:
        user_query.update({"password": password})
        db.commit()
        profile_data = db.query(model.UserProfile).filter(model.UserProfile.user_id==user.id).first()
        if profile_data:
            profile_exist = True
        return {
        "user_id": user.id,
        "profile_exist": profile_exist
        }

    new_user = model.User(**userdata.dict(),username=userdata.email, password=password)
    # adding user to the database
    db.add(new_user)
    db.commit()
    return {
        "user_id": new_user.id,
        "profile_exist": profile_exist
        }



@router.get("/getcurrent_user",response_model=schema.User)
def get_user(db: Session = Depends(get_db),
            current_user: int = Depends(oauth2.get_current_user)):
    return current_user


# @router.post("/block_user")
# def block_user(blocked: schema.BlockedUser, db: Session = Depends(get_db),
#     current_user: int = Depends(oauth2.get_current_user)):
#     already_blocked = db.query(models.BlockUser).filter(
#         models.BlockUser.blocked_user == blocked.user_id,
#         models.BlockUser.blocker_user == current_user.id).first()

#     if already_blocked:
#         return "Already Blocked"

#     status = operation_after_block(db, current_user.id, blocked.user_id)
#     if status:
#         block_obj = model.BlockUser(blocked_user=blocked.user_id, blocker_user=current_user.id)
#         db.add(block_obj)
#         db.commit()
#         db.refresh(block_obj)
#         return block_obj
#     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                         detail="Please try again")


# @router.delete("/unblock_user")
# def unblock_user(blocked: schemas.BlockedUser, db: Session = Depends(get_db),
#     current_user: int = Depends(oauth2.get_current_user)):

#     blocked_query = db.query(models.BlockUser).filter(
#         models.BlockUser.blocked_user == blocked.user_id,
#         models.BlockUser.blocker_user == current_user.id)

#     if blocked_query.first():
#         blocked_query.delete()
#         db.commit()
#         return "unblocked"
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


# @router.post("/report_user")
# def report_user(report_user: schemas.ReportUser, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     report = models.ReportUser(reported_to=report_user.user_id,reported_by=current_user.id, message=report_user.message)
#     db.add(report)
#     db.commit()
#     db.refresh(report)
#     return report


# @router.post("/otp")
# async def send_otp(userdata: schema.UserCreate, db: Session = Depends(get_db)):
#     user_query = db.query(model.User).filter(model.User.email == userdata.email)
#     # temp base set password 123456
#     otp = str(random_with_N_digits(6))
#     password = utils.hash(otp)
#     status = send_otp_mail(userdata.email, otp)
#     profile_exist = False
#     user = user_query.first()
#     if user:
#         user_query.update({"password": password})
#         db.commit()
#         profile_data = db.query(model.UserProfile).filter(model.UserProfile.user_id==user.id).first()
#         if profile_data:
#             profile_exist = True
#         return {
#         "user_id": user.id,
#         "profile_exist": profile_exist
#         }

#     new_user = model.User(**userdata.dict(),username=userdata.email, password=password)
#     # adding user to the database
#     db.add(new_user)
#     db.commit()
#     return {
#         "user_id": new_user.id,
#         "profile_exist": profile_exist
#         }
