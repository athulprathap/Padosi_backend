
import datetime
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,Numeric, true
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import TIMESTAMP
from ..database import  Base , get_db
from typing import Dict
from .. import schema
from ..pydantic_schemas.user import CreateUser
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    # image = Column(String, nullable=False)
    pincode: Integer = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Address(Base):
    __tablename__ = 'address' 
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    housenumber: String = Column(String)
    apartment: String = Column(String)
    city: String = Column(String)
    area: String = Column(String)
    pincode: Integer = Column(Integer, nullable=False)
    state: String=Column(String)
    latitude = Column(Numeric, nullable=True)
    longitude = Column(Numeric, nullable=True)
    user: relationship('User', back_populates='address')
    
class Neighbour(Base):
    __tablename__='neighbour'
    id= Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    pincode: Integer = Column(Integer, nullable=False)
          

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
    

def create_user(user: CreateUser, db: Session,):
    newUser = User(username=user.username, email=user.email, password=user.password)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return newUser


def singleUser(db: Session, id: int):
    
    query_user =  db.query(User).filter(User.id == id).first()
  
    return query_user


def update_user(db: Session,  user: User, id: int, values: Dict={}):
    values['updated_at'] = datetime()
    updated = db.query(User).filter(User.id == id)
    
    updated.update(values)
    db.commit()
    
    return updated.first()


def deactivate_user(current_user: schema.UserList):
    query = "UPDATE my_users SET status='0' WHERE status='1' and email=:email"
    return get_db.execute(query, values= {"email": current_user.email})

def neighbour_user(db:Session, neigh:Neighbour, pincode:int):
    neighbour=db.query(Neighbour).filter(Neighbour.pincode==pincode)
    return neighbour