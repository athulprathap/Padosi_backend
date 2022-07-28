from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, File, UploadFile
from sqlalchemy.orm import Session
from ..import models, schema, oauth2
from ..database import get_db


router = APIRouter( tags = ['Users'])

@router.post("/Register", status_code=status.HTTP_201_CREATED, response_model=schema.UserOpt)
async def create(users: schema.CreateUser, file: UploadFile = File(description="uploadFile"), db:Session = Depends(get_db)):

    hashed_password = utils.hash(users.password)
    users.password = hashed_password
    
    try:
        contents = await file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        await file.close()

    newUser = models.User(**users.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return newUser

@router.get("/users/{id}", response_model=schema.UserOpt)
async def get_user(id:int, db: Session = Depends(get_db),account_owner: int = Depends(oauth2.get_current_user)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"User not found!")

    return user