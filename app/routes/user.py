from fastapi import FastAPI, Response, requests, status, HTTPException, Depends, APIRouter, File, UploadFile
from sqlalchemy.orm import Session
from .. import oauth2
from ..database import get_db
from ..modules.auth.registration import register_new, singleUser, updateUser
from ..pydantic_schemas.user import CreateUser, UserOpt,  User, UserUpdate


router = APIRouter( tags = ['Users'])


@router.post("/Register", status_code=status.HTTP_201_CREATED, response_model=UserOpt)
async def register(user:User, db:Session = Depends(get_db)):
    return register_new(db=db, user=user)


@router.get("/users/{id}", response_model=UserOpt)
async def get_user(id:int, db: Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):
    
    user = singleUser(id=id, db=db)
    
    if user is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found!")
    
    return user


@router.put("/users/{id}", response_model=UserOpt)
async def editUser(id:int, user: UserUpdate , db:Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):
    
    get_update = updateUser(id=id, user=user, db=db, values=dict(user))
    
    if get_update is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= "user with id:{id} does not exist!")
    
    elif  get_update.id != account_owner.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "You can't perform this action!")
    
    
    return get_update