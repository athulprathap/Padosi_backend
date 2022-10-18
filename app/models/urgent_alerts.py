from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from typing import  List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import TIMESTAMP
from ..import oauth2
from ..pydantic_schemas.urgent_alerts import urgent_alerts,Createalert 
from ..models.user import User
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

#Get post of others
def get_others_urgent_alert():
    pass

# Delete a latest alert
def delete(id: int, db: Session, user:int):

    deleted_alert = db.query(urgent_alerts).filter(urgent_alerts == id)
    
    alert = deleted_alert.first()
 
    deleted_alert.delete()
    db.commit()
    
    return alert

# Edit/Update a urgent alert
def update(id:int, alert:Createalert, db: Session , values: Dict={}):

    editedalert = db.query(urgent_alerts).filter(urgent_alerts.id == id)
    
    editedalert.update(values)
    db.commit()

    return editedalert.first()

