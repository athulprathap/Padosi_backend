import jwt
from datetime import datetime, timedelta
from api.utils import constantUtil


async def create_accces_token(*, data: dict, expires_delta: timedelta = None):  # access
    to_encode = data.copy() # encoding data

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=constantUtil.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, constantUtil.SECRET_KEY, algorithm=constantUtil.ALGORITHM)

    return encoded_jwt