from fastapi import FastAPI, Response, requests, status, HTTPException, Depends, APIRouter, File, UploadFile
from sqlalchemy.orm import Session
from .. import schema
from ..models.user import create, singleUser
from ..database import get_db


router = APIRouter( tags = ['Users'])


@router.post("/Register", status_code=status.HTTP_201_CREATED, response_model=schema.UserOpt)
async def register(request:schema.CreateUser, db:Session = Depends(get_db)):
    return create(request, db)


@router.get("/users/{id}")
async def get_user(id:int, db: Session = Depends(get_db)):
    return singleUser(id, db)