from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "039rhfj4994yrcbrt74r47rt7cgrt847r982927847743rtgc98y47n"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 45


def access_token(data: dict):
    to_encode = data.copy()

    expireIn = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    to_encode.update({"exp": expireIn})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt