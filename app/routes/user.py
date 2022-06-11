from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import  get_db
import models, schema, utils


router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schema.UserOpt)
async def create(users: schema.CreateUser, db:Session = Depends(get_db)):

    hashed_password = utils.hash(users.password)
    users.password = hashed_password

    newUser = models.User(**users.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return newUser