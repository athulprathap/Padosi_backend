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


# @router.put("/update/two")
# async def update_scondary_profile(profile_data: schemas.UserProfileTwo,
#     db:Session= Depends(get_db),
#     current_user: int = Depends(oauth2.get_current_user)):
#     data_query = db.query(model.UserProfile).filter(model.UserProfile.user_id==current_user.id)
#     profile = data_query.first()
#     if not profile:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                 detail="User Profile does not exist !!")
#     data_query.update(profile_data.dict(),synchronize_session=False)
#     db.commit()
#     db.refresh(profile)
#     return profile


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

@router.get("/get-notification-detail")
def get_notification_detail( db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    data_query = db.query(model.DeviceToken).filter(model.DeviceToken.user_id==current_user.id)

    return data_query.first()

@router.get("/{profile_id}")
def get_userprofile_by_id(profile_id:int, db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    data_query = db.query(model.UserProfile).filter(model.UserProfile.id==profile_id)
    return data_query.first()



# mobile number api not intergrated
@router.get("/otp")
async def get_otp(db:Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    data = db.query(model.UserProfile).filter(model.UserProfile.user_id==current_user.id).first()
    user_query = db.query(model.User).filter(model.User.id == current_user.id)
    if data:
        otp = random_with_N_digits(6)
        await send_mobile_otp(db, data.mobile, otp)
        otp_expire = utc.localize(datetime.now() + timedelta(minutes=3))
        user_query.update({"passcode":otp,"passcode_expiry_time":otp_expire}, synchronize_session=False)
        db.commit()
        return {"message": "OTP has been sent!!"}
    return "user does not exist!"


@router.post("/mobile/opt-verify")
def get_otp_verify(otp_schema:schema.OtpVerify, db:Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    data_query = db.query(model.UserProfile).filter(model.UserProfile.user_id==current_user.id)
    user_query = db.query(model.User).filter(model.User.id == current_user.id)
    user = user_query.first()
    # if data_query.first():
    #     if "123456" == otp_schema:
    #         if (data_query.first().profile_complete_percent >= 90):
    #             data_query.update({"is_verified": True, "profile_complete_percent":100})
    #         else:
    #             data_query.update({"is_verified": True})
    #         db.commit()
    #         return {"message": "mobile number has been verified !!"}
    #     return {"message": "Wrong OTP !!"}
    # return {"message": "user does not matched"}
    if data_query.first():
        if user.passcode_expiry_time <= utc.localize(datetime.now()):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                detail="otp has been expired !")
        if otp_schema.otp == user.passcode:
            # if (data_query.first().profile_complete_percent >= 85):
            #     data_query.update({"is_verified": True, "profile_complete_percent":100},synchronize_session=False)
            # else:
            #     data_query.update({"is_verified": True}, synchronize_session=False)
            db.commit()
            return {"message": "mobile number has been verified !!"}
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Wrong OTP !!")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                detail="User Nor Matched")


@router.get("/sex/enum")
def get_sex_enum():
    return ["Woman", "Man", "Nonbinary"]


AWS_ACCESS_KEY_ID = config.settings.aws_access_key_id
AWS_SECRET_KEY = config.settings.aws_secret_key
AWS_S3_BUCKET_NAME = config.settings.aws_s3_bucket_name
REGION_NAME='ap-south-1'

# @router.post("/selfie-verification", status_code=status.HTTP_201_CREATED)
# async def post_selfie_verification(file_obj: UploadFile = File(...), db:Session = Depends(get_db),
#     current_user: int = Depends(oauth2.get_current_user)):
#     upload_obj = upload_file_to_bucket(s3_client=s3(),
#                                        file_obj=file_obj.file,
#                                        bucket=AWS_S3_BUCKET_NAME,
#                                        folder=f"{current_user.id}/selfie",  # To Be updated
#                                        object_name=file_obj.filename)

#     data_query = db.query(models.UserProfile).filter(models.UserProfile.user_id==current_user.id)
#     data = data_query.first()
#     if upload_obj:
#         download_url = image_url_substring+f"{current_user.id}/selfie/" +str(file_obj.filename)
#         download_url = download_url.split()
#         download_url = "+".join(download_url)

#         if data:
#             data_query.update({"selfie_image_url": download_url},synchronize_session=False)
#             db.commit()
#             db.refresh(data)
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"selfie image upload failed")

#     is_selfie_verified = await selfie_verification(data.image_url, data.selfie_image_url)
#     if is_selfie_verified:
#         data_query.update({"selfie_verification": True},synchronize_session=False)
#         db.commit()
#         return {"message": "selfie verified"}
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"selfie does not matched")

# ########### with status code ################

# @router.get("/all-delails/recommand/{recommad_id}/{type}")
# def get_all_profile_deltails_by_recommandation(recommad_id:int,type:str, db:Session = Depends(get_db),
#     current_user: int = Depends(oauth2.get_current_user)):
#     recommand = db.query(models.UserRecommadation).filter(
#         models.UserRecommadation.id == recommad_id).first() 
#     user_id = None
#     if type == "WHOLIKE":
#         user_id = recommand.self_user_id
#     else:
#         user_id = recommand.user_id

#     profile = db.query(models.UserProfile).filter(
#         models.UserProfile.user_id==user_id,
#         models.UserProfile.is_deleted==False,
#         ).first()

#     images = db.query(models.Image).filter(
#         models.Image.user_id == user_id,
#         models.Image.is_deleted == False).all()

#     interests_users = db.query(models.UserInterest).filter(
#         models.UserInterest.user_id == user_id).all()
#     interests = []
#     for intr in interests_users:
#         interest = db.query(models.Interest).filter(models.Interest.id == intr.interest_id).first()
#         if interest:
#             interests.append(interest)

#     languages = []
#     languages_user = db.query(models.UserLanguage).filter(
#         models.UserLanguage.user_id == user_id).all()

#     for lang in languages_user:
#         language = db.query(models.Language).filter(models.Language.id == lang.language_id).first()
#         if language:
#             languages.append(language)

#     result_dict = {}
#     result_dict["user_profile"] = profile
#     result_dict["interests"] = interests
#     result_dict["languages"] = languages
#     result_dict["images"] = images
#     result_dict["recommad_id"] = recommad_id
#     return result_dict


# @router.get("/all-delails/{user_id}")
# def get_all_profile_deltails(user_id:int, db:Session = Depends(get_db)):

#     profile = db.query(model.UserProfile).filter(
#         model.UserProfile.user_id==user_id,
#         model.UserProfile.is_deleted==False).first()

#     images = db.query(model.Image).filter(
#         model.Image.user_id == user_id,
#         model.Image.is_deleted == False).all()

#     posts = db.query(model.Post).filter(
#         model.Post.user_id == user_id,
#         model.Post.is_deleted == False
#     ).all()
#     post_list = []
#     for po in posts:
#         interest = db.query(model.Post).filter(model.Post.id == po.id).first()
#         if interest:
#             posts.append(interest)

#     # interests_users = db.query(models.UserInterest).filter(
#     #     models.UserInterest.user_id == user_id).all()
#     # interests = []
#     # for intr in interests_users:
#     #     interest = db.query(models.Interest).filter(models.Interest.id == intr.interest_id).first()
#     #     if interest:
#     #         interests.append(interest)

#     languages = []
#     languages_user = db.query(model.Address).filter(
#         model.Address.user_id == user_id).first()

#     for lang in languages_user:
#         language = db.query(model.Address).filter(model.Address.id == lang.id).all()
#         if language:
#             languages.append(language)


#     result_dict = {}
#     result_dict["user_profile"] = profile
#     # result_dict["posts"] = post_list
#     # result_dict["Address"] = languages
#     # result_dict["images"] = images
#     return result_dict

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
    )

    # query_like = db.query(model.Like).filter(model.Like.post_id == post,user_id)

    address = db.query(model.Address).filter(
        model.Address.user_id==user_id).all()

    # comment = db.query(model.Comment).filter(
    #     model.Comment.user_id==user_id).first()

    # interests_users = db.query(model.UserInterest).filter(
    #     models.UserInterest.user_id == user_id).all()
    # interests = []
    # for intr in interests_users:
    #     interest = db.query(models.Interest).filter(models.Interest.id == intr.interest_id).first()
    #     if interest:
    #         interests.append(interest)

    # languages = []
    # languages_user = db.query(models.UserLanguage).filter(
    #     models.UserLanguage.user_id == user_id).all()

    # for lang in languages_user:
    #     language = db.query(models.Language).filter(models.Language.id == lang.language_id).first()
    #     if language:
    #         languages.append(language)

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

    # images = db.query(model.Image).filter(
    #     model.Image.user_id == user_id,
    #     model.Image.is_deleted == False).all()

    post = db.query(model.Post).filter(
        model.Post.user_id==current_user.id,
        model.Post.is_deleted==False).all()

    address = db.query(model.Address).filter(
        model.Address.user_id==current_user.id).first()

    # comment = db.query(model.Comment).filter(
    #     model.Comment.user_id==user_id).first()

    # interests_users = db.query(model.UserInterest).filter(
    #     models.UserInterest.user_id == user_id).all()
    # interests = []
    # for intr in interests_users:
    #     interest = db.query(models.Interest).filter(models.Interest.id == intr.interest_id).first()
    #     if interest:
    #         interests.append(interest)

    # languages = []
    # languages_user = db.query(models.UserLanguage).filter(
    #     models.UserLanguage.user_id == user_id).all()

    # for lang in languages_user:
    #     language = db.query(models.Language).filter(models.Language.id == lang.language_id).first()
    #     if language:
    #         languages.append(language)

    result_dict = {}
    result_dict["user_profile"] = profile
    result_dict["posts"] = post
    result_dict["Address"] = address
    # result_dict["images"] = images
    return result_dict