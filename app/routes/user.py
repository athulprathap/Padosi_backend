from fastapi import FastAPI, Response, requests, status, HTTPException, Depends, APIRouter, File, UploadFile
from sqlalchemy.orm import Session
from .. import schema, oauth2
from ..models.user import create
from ..database import get_db


router = APIRouter( tags = ['Users'])

# @router.post("/Register", status_code=status.HTTP_201_CREATED, response_model=schema.UserOpt)
# async def create(users: schema.CreateUser, db:Session = Depends(get_db)):

#     hashed_password = utils.hash(users.password)
#     users.password = hashed_password
    
#     newUser = models.User(**users.dict())
#     db.add(newUser)
#     db.commit()
#     db.refresh(newUser)

#     return newUser

@router.post("/Register", status_code=status.HTTP_201_CREATED, response_model=schema.UserOpt)
async def register(request:schema.CreateUser, db:Session = Depends(get_db)):
    return create(request, db)



@router.get("/users/{id}", response_model=schema.UserOpt)
async def get_user(id:int, db: Session = Depends(get_db),account_owner: int = Depends(oauth2.get_current_user)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"User not found!")

    return user