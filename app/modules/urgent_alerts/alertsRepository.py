from fastapi import FastAPI, Response, requests, status, HTTPException, Depends 
from ...model import urgent_alerts, personal_alert, get_others_urgent_alert,create_alert,delete_alert,update_alert
from ...pydantic_schemas.urgent_alerts import urgent_alerts
from typing import  Dict
from sqlalchemy.orm import Session
from ...import oauth2
from ...database import get_db


def create_alert(post:urgent_alerts, db: Session,  user:int= Depends(oauth2.get_current_user)):
    return create_alert(post=post, db=db, user=user)

def myalert(db: Session, user: int = Depends(oauth2.get_current_user)):
    return personal_alert(db=db, user=user)


def get_alert_of_others():
    pass

def get_urgent_alerts_by_id(id:int, db:Session, user:int):
    alert=db.query(urgent_alerts).filter(urgent_alerts.id==id)
    return alert

def get_total_urgent_alerts(id:int, db:Session, user:int):
    alert=[get_urgent_alerts_by_id(id=id,db=db,user=user)]
    return len(alert)

def update_alert(id:int, alert:urgent_alerts, user:int, db: Session, values: Dict={}):
    
    editalert =  update_alert(id=id, alert=create_alert, db=db, values=values)

    if not editalert:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist!")
    
    elif editalert.user_id != user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"You can't perform this action!")
    
    return editalert 


def delete_alert(id: int, db: Session,  user : int = Depends(oauth2.get_current_user)):
    
    destroy = delete_alert(id=id, user=user, db=db)
    
    if not destroy:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post id:{id} does not exist!")

    elif destroy.user_id != user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"You can't perform this action!")
    
    return destroy


