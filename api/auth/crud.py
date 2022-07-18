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

def check_reset_password_token(reset_password_token: str):
    query = "select * from codes where status = '1' and reset_code =:reset_password_token and expired_in > now() at time zone 'UTC' - interval '10 minutes'"
    return database.fetch_one(query, values={"reset_password_token": reset_password_token})

def reset_password(reset_password_token: str, email: str):
    query = "update my_users set password = :password where email = :email"
    return database.execute(query, values={"password": reset_password_token, "email": email})

def disable_reset_code(reset_password_token: str, email: str):
    query = "update codes set status = '0' where reset_code = :reset_password_token and email = :email"
    return database.execute(query, values={"reset_password_token": reset_password_token, "email": email})