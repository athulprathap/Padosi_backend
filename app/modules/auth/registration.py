from fastapi import FastAPI, Response, requests, status, HTTPException, Depends
from ...models.user import create_user, singleUser, update_user
from sqlalchemy.orm import Session
from ...pydantic_schemas.user import User
from ...import utils
from ...import oauth2
from ...database import get_db


def register_new(user: User, db: Session):
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    return create_user(user=user, db=db)


def single_user(id: int, db: Session):
    return singleUser(db, id)
 

def updateUser(user: User, id:int, db: Session):
    update_user(db)