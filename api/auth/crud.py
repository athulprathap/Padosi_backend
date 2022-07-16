from api.utils.dbUtil import database
from api.auth import schemas

def find_existed_user(email: str):
    query = "select * from my_users where email=:email and status='1'"
    return database.fetch_one(query, values={"email": email})

def save_user(user: schemas.UserCreate):
    query = "INSERT INTO my_users VALUES (nextval('user_id_seq'), :email, :password, :fullname, now() at time zone 'UTC', '1')"
    return database.execute(query, values={"email": user.email, "password": user.password, "fullname": user.fullname})

def create_reset_code(email: str, reset_code: str):
    query = "INSERT INTO codes VALUES (nextval('code_id_seq'), :email, :reset_code, now() at time zone 'UTC','1')"
    return database.execute(query, values={"email": email, "reset_code": reset_code})
