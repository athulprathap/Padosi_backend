from .. import model, schema, oauth2
from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from ..utils import  push_notification
from sqlalchemy import func


router = APIRouter(
    prefix="/notifications",
    tags=['Notification']
)


@router.put("",status_code=201)
def is_notification_enable(is_enable: bool,db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    data_query = db.query(model.DeviceToken).filter(model.DeviceToken.user_id==current_user.id)
    if data_query.first():
        data_query.update({"is_enable":is_enable}, synchronize_session=False)
        db.commit()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="notification data not found !!")


@router.put("/device/token", status_code=201)
def create_device_token(token_data: schema.DeviceToken, db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    data_query = db.query(model.DeviceToken).filter(model.DeviceToken.user_id==current_user.id)
    if data_query.first():
        data_query.update(token_data.dict(), synchronize_session=False)
        db.commit()
        return data_query.first()
    data = model.DeviceToken(**token_data.dict(), user_id=current_user.id)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


@router.get("/get-device-status", status_code=201)
def get_user_device_token(db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    data = db.query(model.DeviceToken).filter(model.DeviceToken.user_id==current_user).first()
    if data:
        return data
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="notification data not found !!")


@router.put("/preview-message", status_code=201)
def is_preview_message_enable(is_enable: bool,db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    data_query = db.query(model.DeviceToken).filter(model.DeviceToken.user_id==current_user.id)
    if data_query.first():
        data_query.update({"message_preview":is_enable}, synchronize_session=False)
        db.commit()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="notification data not found !!")


@router.get("/test")
async def test_notification():
    # sanket device token
    token = "csz-e383Q-muvAk7n-_5lX:APA91bHEIAwwJvQcTSLrsq2I8elFwmdNkCGD78rlVnwNPI_HJqw_Ft1KsdNvh6XKK89RZgvHSRkSZUog8VTxPYw51NclTq0XhOSMKJjX2Q2YLY2GtM1y5PD0QaQjxtui37fBzjfV2Qze"
    data = {
        "title": "Title message",
        "message": "Body message it can be delailed"
    }
    status = await push_notification(token, data)
    if status:
        return "message has been sent!!"
    return "notification failed"
