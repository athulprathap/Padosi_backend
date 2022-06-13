from fastapi import FastAPI, APIRouter, Response, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_db
import schema, models, utils, oauth2

router = APIRouter(tags = ['Login'])

@router.post('/login')
async def login_user(user_info: schema.UserAuth, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_info.email).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials!")
    
    if not utils.verify(user_info.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    token = oauth2.access_token(data={"user_id": user.id})

    return {"access_token": token, "token_type":"bearer"}