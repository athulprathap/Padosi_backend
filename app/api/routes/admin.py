from fastapi import APIRouter, Depends, status, HTTPException, Response, UploadFile, File
from sqlalchemy.orm import Session
from app.api.database import get_db
from .. import model, schema, utils, oauth2, config
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. utils import send_otp_mail, random_with_N_digits, verify_otp
from typing import List, Optional, Union
from ..modules.userRepository import register_new, updateUser, singleUser, admin_register_new
from ..schema import UserOpt,  User, UserUpdate


router = APIRouter(
    prefix="/admin",
    tags=['Admin-App']
)


# @router.post("/Register", status_code=status.HTTP_201_CREATED, response_model=schema.admin)
# async def register(user:User, db:Session = Depends(get_db)):

#     return admin_register_new(db=db, user=user)

@router.post("/verify-otp-register", status_code=status.HTTP_201_CREATED)
async def verify_otp_resgister(user: User, db: Session = Depends(get_db)):
    status = await verify_otp(user.mobile, user.otp)
    if status == "approved":
        return admin_register_new(db=db, user=user)
        db.query(model.User).filter(model.User.is_admin == True)
    else:
        return ("Unable to verify OTP")


@router.post("/login")
def admin_login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(model.User).filter(
        model.User.email == user_credentials.username,
        model.User.is_deleted == False,
        model.User.is_admin == True).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User doesn't exist ")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Wrong OTP!! Please try again")

    access_token = oauth2.access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/all_user/")
def get_all_user(db: Session = Depends(get_db)):
    # userid=db.query(model.User).filter(model.User.id).all()
    # print(userid)(model.User).filter(model.User.id == userid).first()
    # user = db.query
    # while True:
    cusers = db.query(model.User,model.UserProfile,model.Address).join(model.UserProfile,model.User.id==model.UserProfile.user_id).join(model.Address,model.User.id==model.Address.user_id).filter(model.User.is_admin == False).all()
    cusersids = []
    for cuser in cusers:
        userprofile = cuser[0].__dict__
        user = cuser[1].__dict__
        address = cuser[2].__dict__
        userprofile["user"]=user
        userprofile["address"]=address
        cusersids.append(userprofile)
        return cusersids

        # profile = db.query(model.UserProfile).filter(
        #     model.UserProfile.user_id == cuser.__getattribute__("id")).first()
        # if not profile:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        # address = db.query(model.Address).filter(
        #     model.Address.user_id == cuser.__getattribute__("id")).first()
        # if not address:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        # x = cuser.__dict__
        # del x['password']
        # del x['passcode']
        # del x['passcode_expiry_time']
        # del x ['is_admin']
        # x["area"] = address.__getattribute__("area")
        # x["city"] = address.__getattribute__('city')
        # x["profile_pic"] = profile.__getattribute__('image_url')
        # x["fullname"] = profile.__getattribute__('full_name')
        # cusersids.append(cuser)
        return cusersids
    # x = db.query(model.User).filter(model.User.id).all()
    # status = []
    # pro = []
    # add=[]
    # while (True):
    #     i = 0
    #     print(i)
    #     i = i+1
    #     for x in users:
    #         interest = db.query(model.User).filter(model.User.id == x.status).first()
    #         if interest:
    #             status.append(interest)
    #     for y in profile:
    #         # profile = db.query(model.UserProfile).filter(model.UserProfile.user_id == x.).all()
    #         query = db.query(model.UserProfile).filter(model.UserProfile.user_id == y.mobile).first()
    #         if query:
    #             pro.append(query)
    #     for z in address:
    #         data = db.query(model.Address).filter(model.Address.user_id == z.area).first()
    #         if data:
    #             add.append(query)

    #     result_dict = {}
    #     result_dict["status"] = status
    #     result_dict["profile"] = pro
    #     result_dict["address"] = add
    #     return result_dict
    #     cusers  = cusers + 1


@router.get("/admin-profile")
def get_profile(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(model.User).filter(model.User.id == current_user.id)
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found")
    return user


@router.get("/reported_post")
def report_user(db: Session = Depends(get_db)):
    cusers = db.query(model.ReportPosts).all()
    if cusers == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found")
    cusersids = []
    for cuser in cusers:
        cusersids.append(cuser.__getattribute__("id"))
        post = db.query(model.Post).filter(model.Post.id ==
                                           cuser.__getattribute__("post_id")).first()
        r_p_user = post.__getattribute__("user_id")
        print(r_p_user)
        profile = db.query(model.UserProfile).filter(
            model.UserProfile.user_id == cuser.__getattribute__("reported_by")).first()
        rprofile = db.query(model.UserProfile).filter(
            model.UserProfile.user_id == r_p_user).first()
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        users = db.query(model.ReportPosts).filter(
            model.ReportPosts.post_id == cuser.__getattribute__("post_id")).first()
        # result_dict = {}
        # result_dict["user_profile"] = profile
        # result_dict["posts"] = post
        # result_dict["Address"] = address
        # # result_dict["images"] = images
        # return result_dict
        return {
            "status": users.__getattribute__('status'), 
            "message": users.__getattribute__('message'),
            "post_id": users.__getattribute__('post_id'),
            "reported_user_image_url": profile.__getattribute__('image_url'),
            "reported_user_full_name": profile.__getattribute__('full_name'),
            "reporting_user_image_url": rprofile.__getattribute__('image_url'),
            "reporting_user_full_name": rprofile.__getattribute__('full_name'),
            "category": "post"
        }


@router.get("/get-all-alerts")
def alerts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(model.urgent_alerts).all()
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found")
    return user


@router.get("/get-all-post-userid/{user_id}")
def post_user(user: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(model.Post).filter(model.Post.user_id == user).all
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found")
    return user


@router.put("/block")
def block_user(id: int, db: Session = Depends(get_db),
               current_user: int = Depends(oauth2.get_current_user)):
    value = db.query(model.User).filter(model.User.id == id).first()
    new = value.__getattribute__("is_blocked")

    if new:
        block = db.query(model.User).filter(
            model.User.id == id).update({'is_blocked': False})
        if current_user.is_admin:
            db.commit()
            return block
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        block = db.query(model.User).filter(
            model.User.id == id).update({'is_blocked': True})
        if current_user.is_admin:
            db.commit()
            return block
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/change_address")
def change_address(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(model.ChangeAddress).all()
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found")
    cusersids = []
    for cuser in user:
        cusersids.append(cuser.__getattribute__("id"))
        post = db.query(model.Address).filter(model.Address.user_id ==
                                           cuser.__getattribute__("user_id")).first()
        r_p_user = post.__getattribute__("area")
        r_p_user2 = post.__getattribute__("city")
        print(r_p_user)
        profile = db.query(model.UserProfile).filter(
            model.UserProfile.user_id == cuser.__getattribute__("user_id")).first()
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        users = db.query(model.ChangeAddress).filter(
            model.Address.user_id == cuser.__getattribute__("user_id")).first()
    return {
            "status": users.__getattribute__('status'), 
            "change_to_area": users.__getattribute__('change_area'),
            "change_to_city": users.__getattribute__('change_city'),
            "user_image": profile.__getattribute__('image_url'),
            "user_fullname": profile.__getattribute__('full_name'),
            "recent_area":r_p_user,
            "recent_city":r_p_user2
        }



@router.put("/address_change")
def address_change(id: int, allaow: schema.AdminPermission, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    permission = db.query(model.ChangeAddress).filter(
        model.ChangeAddress.user_id == id).first()
    new = permission.__getattribute__("allowance")
    status = permission.__getattribute__("status")

    if new:
        block = db.query(model.ChangeAddress).filter(
            model.ChangeAddress.user_id == id).update({'allowance': False})
        block = db.query(model.ChangeAddress).filter(
            model.ChangeAddress.user_id == id).update({'status': "REJECTED"})
        if current_user.is_admin:
            db.commit()
            return block
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        block = db.query(model.ChangeAddress).filter(
            model.ChangeAddress.user_id == id).update({'allowance': True})
        block = db.query(model.ChangeAddress).filter(
            model.ChangeAddress.user_id == id).update({'status': "Resolved"})
        if current_user.is_admin:
            db.commit()
            return block
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
