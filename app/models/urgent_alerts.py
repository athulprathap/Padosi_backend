from Padosi_backend.app.dbmanager import get_tokens
from fastapi import FastAPI, Response, status, HTTPException, Depends
from requests import session
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from typing import  List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import TIMESTAMP
from ..import oauth2
from ..pydantic_schemas.urgent_alerts import urgent_alerts,Createalert 
from .user import Address, User, neighbour_user, Neighbour
from ..database import get_db, Base
from ..notify.ncrud import get_tokens
from ..routes.notifications import is_notification_enable, get_user_device_token, create_device_token, is_preview_message_enable

class urgent_alerts(Base):
    __tablename__ = "urgent_alerts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")
    
class respond_to_alerts(Base):
    __tablename__="response"
    id=Column(Integer, ForeignKey("urgent_alerts.id", ondelete="CASCADE"),primary_key=True)
    respond=Column(String, nullable=False)

class DeviceToken(Base):
    _tablename_ = "device_token"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    token = Column(String, nullable=False)
    is_enable = Column(Boolean, server_default="TRUE", nullable=True)
    message_preview = Column(Boolean, server_default= "TRUE", nullable= True)
    pincode: Integer = Column(Integer, nullable=False)

def add_into_tokens_table(user:int, db:Session):
    tokenn=get_tokens(user_id=oauth2.get_current_active_user)
    t=DeviceToken(tokenn=DeviceToken.token, user=user)
    db.add(t)
    db.commit()
    db.refresh(t)
    
def get_tokens_of_neighbour(user:int, db:Session):
    res=db.query(DeviceToken).filter(DeviceToken.pincode==user.pincode).all()
    return res

        
# Get only my alert

def personal_alert(db: Session, user:int):
    owner_urgent_alert = db.query(urgent_alerts).filter(urgent_alerts.user_id == user.id).all()
    return  owner_urgent_alert
    
# respond to alerts

def create_response(id:int,response:respond_to_alerts, db:Session, user:int):
    res=respond_to_alerts(respond=response.respond, user=user)
    
    db.add(res)
    db.commit()
    db.refresh(res)
    
    return res

def get_response(user:int,db:Session):
    res=db.query(respond_to_alerts).filter(respond_to_alerts.id==user.id).all()
    return res

# Create a new alert
def create_alert(alert:urgent_alerts, db: Session, user: int):
    newalert = urgent_alerts( title=alert.title, content=alert.content, published=alert.published, user=user)
    db.add(newalert)
    db.commit()
    db.refresh(alert)
    
    return alert

def get_urgent_alerts_by_id(id:int, db:Session, user:int):
    alert=db.query(urgent_alerts).filter(urgent_alerts.id==id)
    return alert

def get_total_urgent_alerts(id:int, db:Session, user:list):
    alert=[get_others_urgent_alert(id=id,db=db,user=neighbour_user)]
    return len(alert)

#get neighbour user
def neighbour_user(db:Session,pincode:int):
    neighbour=neighbour_user(db=db,pincode=pincode)
    return neighbour
    

#Get post of others
def get_others_urgent_alert(id:int, db:Session, user:int):
    alert=[get_urgent_alerts_by_id(id=id,db=db,user=neighbour_user)]
    return alert
    

# Delete a latest alert
def delete_alert(id: int, db: Session, user:int):

    deleted_alert = db.query(urgent_alerts).filter(urgent_alerts == id)
    
    alert = deleted_alert.first()
 
    deleted_alert.delete()
    db.commit()

    return alert

# Edit/Update a urgent alert
def update_alert(id:int, alert:Createalert, db: Session , values: Dict={}):

    editedalert = db.query(urgent_alerts).filter(urgent_alerts.id == id)
    
    editedalert.update(values)
    db.commit()

    return editedalert.first()




