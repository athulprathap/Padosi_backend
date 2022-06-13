from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import  get_db
import models, schema, utils


router = APIRouter( tags = ['Users'])

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schema.UserOpt)
async def create(users: schema.CreateUser, db:Session = Depends(get_db)):

    hashed_password = utils.hash(users.password)
    users.password = hashed_password

    newUser = models.User(**users.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return newUser

@router.get("/users/{id}", response_model=schema.UserOpt)
async def get_user(id:int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"User not found!")

    return user