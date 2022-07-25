from fastapi import FastAPI, APIRouter, Response, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import  database, schema, models, utils, oauth2

router = APIRouter(tags = ['Login'])

@router.post('/login', response_model=schema.Token)
async def login_user(user_info: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_info.username).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials!")
    
    if not utils.verify(user_info.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    token = oauth2.access_token(data={"users_id": user.id})

    return {"access_token": token, "token_type":"bearer"}