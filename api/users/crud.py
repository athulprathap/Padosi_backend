from api.utils.dbUtil import database
from api.users import schemas as users_schemas
from api.auth import schemas as auth_schemas

def update_user(
    request: users_schemas.UserUpdate, 
    current_user: auth_schemas.UserList):
    
    query = "UPDATE my_users SET fullname=:fullname where email=:email"

    return database.execute(query, values= {"fullname": request.fullname, "email": current_user.email})

def deactivate_user(current_user: auth_schemas.UserList):
    query = "UPDATE my_users SET status='0' WHERE status='1' and email=:email"
    return database.execute(query, values= {"email": current_user.email})