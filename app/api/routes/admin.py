from fastapi import APIRouter, Depends, status, HTTPException, Response, UploadFile, File
from sqlalchemy.orm import Session
from app.api.database import get_db
from .. import model, schema, utils, oauth2, config
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. utils import send_otp_mail, random_with_N_digits,verify
from typing import List, Optional,Union
from ..modules.userRepository import admin_register_new, updateUser,singleUser
from ..schema import UserOpt,  User, UserUpdate


router = APIRouter(
    prefix="/admin",
    tags=['Admin-App']
)



@router.post("/Register", status_code=status.HTTP_201_CREATED, response_model=UserOpt)
async def register(user:User, db:Session = Depends(get_db)):
    
    return admin_register_new(db=db, user=user)

@router.post("/login")
def admin_login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    user = db.query(model.User).filter(
        model.User.username == user_credentials.username,
        model.User.is_deleted == False,
        model.User.is_admin == True).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User doesn't exist ")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Wrong OTP!! Please try again")

    access_token = oauth2.access_token(data = {"user_id": user.id})
    return {"access_token" : access_token, "token_type": "bearer"}

@router.get("/all_user")
def get_all_user(db: Session=Depends(get_db)):
    user = db.query(model.User).all()
    return user

@router.get("/reported_user")
def report_user(db: Session=Depends(get_db)):
    user = db.query(model.ReportUser).all()
    return user

@router.put("/block")
def block_user(id:int,db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    value = db.query(model.User).filter(model.User.id == id).first()
    new = value.__getattribute__("is_blocked")
    
    if new:
        block = db.query(model.User).filter(model.User.id==id).update({'is_blocked': False})
        if current_user.is_admin:
            db.commit()
            return block
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        block = db.query(model.User).filter(model.User.id==id).update({'is_blocked': True})
        if current_user.is_admin:
            db.commit()
            return block
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@router.get("/change_address")
def change_address(db: Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(model.ChangeAddress).all()
    return user

@router.put("/address_change")
def address_change(id:int,allaow:schema.AdminPermission,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    permission = db.query(model.ChangeAddress).filter(model.ChangeAddress.user_id == id).first()
    new = permission.__getattribute__("allowance")
    status = permission.__getattribute__("status")

    if new:
        block = db.query(model.ChangeAddress).filter(model.ChangeAddress.user_id==id).update({'allowance': False})
        block = db.query(model.ChangeAddress).filter(model.ChangeAddress.user_id==id).update({'status': "REJECTED"})
        if current_user.is_admin:
            db.commit()
            return block
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        block = db.query(model.ChangeAddress).filter(model.ChangeAddress.user_id==id).update({'allowance': True})
        block = db.query(model.ChangeAddress).filter(model.ChangeAddress.user_id==id).update({'status': "Resolved"})
        if current_user.is_admin:
            db.commit()
            return block
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

