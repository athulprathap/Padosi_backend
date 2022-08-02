from fastapi import FastAPI, Response, requests, status, HTTPException, Depends, APIRouter, File, UploadFile
from sqlalchemy.orm import Session
from .. import oauth2
from ..database import get_db
from ..modules.auth.registration import register_new, singleUser
from ..pydantic_schemas.user import CreateUser, UserOpt,  User


router = APIRouter( tags = ['Users'])


@router.post("/Register", status_code=status.HTTP_201_CREATED, response_model=UserOpt)
async def register(user:User, db:Session = Depends(get_db)):
    return register_new(db=db, user=user)


@router.get("/users/{id}")
async def get_user(id:int, db: Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):
    return singleUser(id=id, db=db)

@router.put("/users/{id}", response_model=UserOpt )
async def editUser(id, request: User ,db:Session = Depends(get_db)):
    return update(id, request, db)