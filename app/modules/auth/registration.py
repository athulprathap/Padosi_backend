from ...models.user import create_user, singleUser, update_user
from fastapi import FastAPI, Response, requests, status, HTTPException, Depends
from sqlalchemy.orm import Session
# from model import create_user, update_user
from ...pydantic_schemas.user import User
from ...import utils
from ...import oauth2


def register_new( user: User, db: Session):
    # update_user(db=db, id=1, values={'username': 'seun'})
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    return create_user(user=user, db=db)



def single_user(id: int, db: Session,  account_owner: int = Depends(oauth2.get_current_user)):
    user = singleUser(id=id, db=db)
    if user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"User not found!")
    else:
        return user
 