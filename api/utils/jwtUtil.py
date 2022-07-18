import jwt
from jwt import PyJWTError, InvalidTokenError
from pydantic import ValidationError 
from datetime import datetime, timedelta
from api.utils import constantUtil
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from api.auth import crud, schemas

async def create_accces_token(*, data: dict, expires_delta: timedelta = None):  # access
    to_encode = data.copy() # encoding data

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=constantUtil.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, constantUtil.SECRET_KEY, algorithm=constantUtil.ALGORITHM)

    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='api/v1/auth/login',
)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, constantUtil.SECRET_KEY, algorithms=[constantUtil.ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        
        # check if user exists
        result = await crud.find_existed_user(username)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return schemas.UserList(**result)


    except (PyJWTError, ValidationError):
        raise credentials_exception 


def get_current_active_user(current_user: schemas.UserList = Depends(get_current_user)):
    if current_user.status != "1":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not active")
    
    return current_user

