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
    
# Get only my alert

def personal_alert(db: Session, user:int):
    owner_urgent_alert = db.query(urgent_alerts).filter(urgent_alerts.user_id == user.id).all()
    return  owner_urgent_alert
    
    
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
    return [neighbour]
    

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

def respond_to_alert(id:int, user:int, alert:urgent_alerts):
    pass

