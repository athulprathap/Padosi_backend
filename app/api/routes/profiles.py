from sqlalchemy import func

from fastapi import Depends, status, HTTPException, APIRouter, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from app.api.database import get_db
from app.api import model,schema,oauth2,config
from .. utils import calculateAge
from sqlalchemy import func
from . imagesupload import upload_file_to_bucket, s3, image_url_substring
from datetime import datetime, timedelta
import pytz
from ..utils import random_with_N_digits, send_mobile_otp

utc=pytz.UTC


router = APIRouter(
    prefix="/profiles",
    tags=['Profile']
)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_profile(profile_data: schema.UserProfile,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    data = db.query(model.User).filter(model.User.id==current_user.id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user with id: {current_user.id} does not exist")
    profile = model.UserProfile(**profile_data.dict(),age=calculateAge(profile_data.date_of_birth),user_id=current_user.id)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.put("/update/one")
async def update_scondary_profile(profile_data: schema.UserProfileOne,
    db:Session= Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    data_query = db.query(model.UserProfile).filter(model.UserProfile.user_id==current_user.id)
    userprofile = data_query.first()
    if not userprofile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail="User Profile does not exist !")
    data_query.update(profile_data.dict(),synchronize_session=False)
    db.commit()
    db.refresh(userprofile)
    return userprofile


@router.put("/name/update")
def update_name(full_name:str,db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    profile_query = db.query(model.UserProfile).filter(
            model.UserProfile.user_id == current_user.id)
    profile = profile_query.first()
    if profile:
        if (profile.name_change_date <= utc.localize(datetime.today() - timedelta(days=90))):
            profile_query.update({"full_name":full_name, "name_change_date": datetime.today()}, synchronize_session=False)
            db.commit()
            return {"message": "Success"}
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"You can change name once in 3 months")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail= "Profile not found")


@router.put("/mobile")
async def update_mobile(schema_mobile: schema.Mobile,db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    data_query = db.query(model.UserProfile).filter(model.UserProfile.user_id==current_user.id)
    data_query.update({"mobile":schema_mobile.mobile, "is_verified": False}, synchronize_session=False)
    user_query = db.query(model.User).filter(model.User.id==current_user.id)
    otp = random_with_N_digits(6)
    await send_mobile_otp(db, schema_mobile.mobile, otp)
    otp_expire = utc.localize(datetime.now() + timedelta(minutes=3))
    user_query.update({"passcode":otp,"passcode_expiry_time":otp_expire}, synchronize_session=False)
    db.commit()
    return data_query.first()


@router.delete("/delete")
def delete_profile(db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    user_data_query = db.query(model.User).filter(model.User.id==current_user.id,
        model.User.is_deleted == False)
    # user_profile_data_query = db.query(models.UserProfile).filter(models.UserProfile.user_id == current_user.id,
    #     models.UserProfile.is_deleted == False)

    # if user_profile_data_query.first():
    #     user_profile_data_query.update({"is_deleted": True}

    if user_data_query.first():
        user_data_query.delete()
        db.commit()
        return {"user has been deleted"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User already does not exist")


@router.get("/byuserid/{user_id}")
def get_userprofile_by_userid(user_id:int, db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    data_query = db.query(model.UserProfile).filter(model.UserProfile.user_id==user_id)
    return data_query.first()


@router.get("/{profile_id}")
def get_userprofile_by_id(profile_id:int, db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    data_query = db.query(model.UserProfile).filter(model.UserProfile.id==profile_id)
    return data_query.first()


@router.get("/sex/enum")
def get_sex_enum():
    return ["Woman", "Man", "Nonbinary"]


@router.get("/all-delails/{user_id}")
def get_all_profile_deltails(user_id:int, db:Session = Depends(get_db)):

    profile = db.query(model.UserProfile).filter(
        model.UserProfile.user_id==user_id,
        model.UserProfile.is_deleted==False).first()

    # images = db.query(model.Image).filter(
    #     model.Image.user_id == user_id,
    #     model.Image.is_deleted == False).all()

    post = db.query(model.Post, func.count(model.Like.post_id).label("likes")).join(model.Like, model.Like.post_id == model.Post.id,
            isouter=True).group_by(model.Post.id).filter(
        model.Post.user_id==user_id,
        model.Post.is_deleted==False).all()

    comments = db.query(model.Comment).filter(
        model.Comment.user_id == user_id
    ).first()

    # query_like = db.query(model.Like).filter(model.Like.post_id == post,user_id)

    address = db.query(model.Address).filter(
        model.Address.user_id==user_id).first()

    result_dict = {}
    result_dict["user_profile"] = profile
    result_dict["posts"] = post
    result_dict["Address"] = address
    # result_dict["comment"] = comments

    return result_dict

@router.get("/all-delails-current-user")
def get_all_profile_deltails(db:Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    profile = db.query(model.UserProfile).filter(
        model.UserProfile.user_id==current_user.id,
        model.UserProfile.is_deleted==False).first()

    post = db.query(model.Post, func.count(model.Like.post_id).label("likes")).join(model.Like, model.Like.post_id == model.Post.id,
            isouter=True).group_by(model.Post.id).filter(
        model.Post.user_id==current_user.id,
        model.Post.is_deleted==False).all()

    address = db.query(model.Address).filter(
        model.Address.user_id==current_user.id).first()


    result_dict = {}
    result_dict["user_profile"] = profile
    result_dict["posts"] = post
    result_dict["Address"] = address
    # result_dict["images"] = images
    return result_dict