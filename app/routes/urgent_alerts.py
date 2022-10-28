from operator import ge
from fastapi import FastAPI, Response, requests, status, HTTPException, Depends, APIRouter, File, UploadFile
from sqlalchemy.orm import Session
from app.models.urgent_alerts import create_response, get_others_urgent_alert, get_response
from app.models.user import neighbour_user
from ..routes.notifications import is_notification_enable, is_preview_message_enable, create_device_token, get_user_device_token
from ..utils import  push_notification
from app.pydantic_schemas.urgent_alerts import urgent_alerts
from .. import oauth2
from .. import model,schema
from ... import FCMmanager
from ..pydantic_schemas.posts import Post, PostAll, PostOpt, CreatePost, Likes
from sqlalchemy import func
from ..database import get_db
from ..modules.users.userRepository import register_new, singleUser, updateUser
from ..modules.urgent_alerts.alertsRepository import create_alert, myalert, update_alert, get_alert_of_others, delete_alert,get_urgent_alerts_by_id,get_total_urgent_alerts
from ..pydantic_schemas.user import CreateUser, UserOpt,  User, UserUpdate
import os


router = APIRouter(tags = ['urgent_alerts'])

@router.get("/urgent-alerts")
async def get_all_urgent_alerts(id:int, db:Session =Depends(get_db),user: int = Depends(oauth2.get_current_user)):
    return get_others_urgent_alert(id=id, db=db, user=neighbour_user)

@router.post("/urgent-alerts", status_code=status.HTTP_201_CREATED,  response_model=PostOpt)
async def create_new_urgent_alerts(alert:urgent_alerts, db: Session = Depends(get_db), user:int= Depends(oauth2.get_current_user)):
    tokens=get_tokens_of_neighbour(user=user, db=db)
    converted_tokens = [value for (value,) in tokens]
    FCMmanager.send(msg="A new urgent alert has been created from your neighbour",title="Urgent alert",body="A new urgent alert in the neighbourhood",tokens=converted_tokens)
    return create_alert(db=db, alert=alert, user=user)

@router.get("/urgent-alerts/count")
async def get_number_of_urgent_alerts(id:int, db:Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    return get_total_urgent_alerts(id=id,db=db,user=user)

@router.get("/urgent-alerts/{id}")
async def find_urgent_alert_by_id(id:int, db:Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    return get_urgent_alerts_by_id(id=id, db=db, user=user)

@router.put("/urgent-alerts/{id}", status_code=status.HTTP_201_CREATED,  response_model=PostOpt)
async def update_urgent_alert(id:int, alert:create_alert, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    return update_alert(id=id, alert=alert, user=user, db=db, values=dict(alert))

@router.delete("/urgent-alerts/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_urgent_alerts(id: int, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):    
    return delete_alert(id=id, db=db, user=user)

@router.post("/urgent-alerts/{id}/respond")
async def respond_to_urgent_alerts(id:int, db:Session= Depends(get_db), user: int= Depends(oauth2.oauth2.get_current_user)):
    if urgent_alerts:
        tokens=get_tokens_of_neighbour(user=user, db=db)
        converted_tokens = [value for (value,) in tokens]
        FCMmanager.send(msg="A new urgent alert response has been created from your neighbour",title="Urgent alert",body="A new urgent alert response in the neighbourhood",tokens=converted_tokens)
        return create_response(response=respond_to_urgent_alerts, db=db, user=neighbour_user)

@router.get("/urgent-alerts/{id}/respond")
async def get_response_of_urgent_alerts(id:int, db:Session= Depends(get_db), user: int= Depends(oauth2.oauth2.get_current_user)):
    tokenn=get_user_device_token(db=db)
    send_notification_to_neighbours(user=user, db=db)
    return get_response(user=user, db=db)
    