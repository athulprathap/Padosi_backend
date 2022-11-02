from fastapi import FastAPI, Response, requests, status, HTTPException, Depends
from ..crud import create_user, singleUser, update_user
from sqlalchemy.orm import Session
from app.api.schema import User
from ..import utils
from  ..oauth2 import get_current_user,get_current_active_user
from ..database import get_db
from typing import Dict


def register_new(user: User, db: Session):
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    return create_user(user=user, db=db)


def single_user(id: int, db: Session):
    return singleUser(db, id)
 

def updateUser(id:int, user:User, db: Session, values: Dict={}):
    return update_user(db=db, user=user, id=id, values=values)