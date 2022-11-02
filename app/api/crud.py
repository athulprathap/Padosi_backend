import datetime
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.api.database import get_db
from typing import Optional, Dict
from . import schema
from sqlalchemy import func
from .model import Post,Like,User
from .schema import Likes,Post,CreatePost,CreateUser,UserDevicePayload, MessagePayload, Response, ErrorResponse
from sqlalchemy.orm import relationship
# from . import dbmanager,FCMmanager


def personal_post(db: Session, user:int):
    owner_post = db.query(Post).filter(Post.user_id == user.id).all()
    return  owner_post


# Create a post
def create(post:Post, db: Session, user: int):
    newPost = Post( title=post.title, content=post.content, published=post.published, user=user)
    
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    
    return newPost


# Get all post
def allPost(db: Session, limit:int = 9, skip:int = 0, option: Optional[str] = ""):
    # join tables and get the results
    allPost  = db.query(Post, func.count(Like.post_id).label("likes")).join(Like, Like.post_id == Post.id,
            isouter=True).group_by(Post.id).filter(Post.title.contains(option)).limit(limit).offset(skip).all()
        
    return allPost 


    # Like and Unlike a post
def like_unlike(db: Session , like: Likes,  user: int):
        
       query_like = db.query(Like).filter(Like.post_id == like.post_id, Like.user_id == user.id)
       
       isLiked = query_like.first()
       
       query_like.delete(synchronize_session=False)
       db.commit()
    
       return isLiked 


# Get a post
def singlePost(id:int, db:Session):
    
    single_post = db.query(Post, func.count(Like.post_id).label("likes")).join(Like,
                 Like.post_id == Post.id, isouter=True).group_by(Post.id).filter(Post.id == id).first()

    return single_post
    
    
# Delete a Post
def delete(id: int, db: Session, user:int):

    deleted_post = db.query(Post).filter(Post.id == id)
    
    post = deleted_post.first()
 
    deleted_post.delete()
    db.commit()
    
    return post


# Edit/Update a Post
def update(id:int, post:CreatePost, db: Session , values: Dict={}):

    editedPost = db.query(Post).filter(Post.id == id)
    
    editedPost.update(values)
    db.commit()

    return editedPost.first()


def create_user(user: CreateUser, db: Session,):
    newUser = User(username=user.username, email=user.email, password=user.password)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return newUser


def singleUser(db: Session, id: int):
    
    query_user =  db.query(User).filter(User.id == id).first()
  
    return query_user


def update_user(db: Session,  user: User, id: int, values: Dict={}):
    values['updated_at'] = datetime()
    updated = db.query(User).filter(User.id == id)
    
    updated.update(values)
    db.commit()
    
    return updated.first()


def deactivate_user(current_user: schema.UserList):
    query = "UPDATE my_users SET status='0' WHERE status='1' and email=:email"
    return get_db.execute(query, values= {"email": current_user.email})



# async def save(user_device: UserDevicePayload) -> Dict:
#     last_record_id = await dbmanager.save(user_devices, user_device)

#     return {**user_device.dict(), "id": last_record_id}


# async def get_tokens(user_id) -> List[Mapping]:
#     tokens = await dbmanager.get_tokens(user_devices, user_id)

#     return tokens


# async def send(message: MessagePayload) -> Response:
#     tokens = await get_tokens(message.user_id)
#     converted_tokens = [value for (value,) in tokens]

#     if len(converted_tokens) == 0:
#         raise HTTPException(status_code=404,
#                             detail=f'user id {message.user_id} don\'t have any registered device(s)')

#     batch_response = FCMmanager.send(message.message,
#                                   message.notify.get("title"),
#                                   message.notify.get("body"),
#                                   converted_tokens
#                                   )
#     errors_lst = []
#     for v in batch_response.responses:
#         if v.exception:
#             error = {}
#             cause_resp = v.exception.__dict__.get("_cause").__dict__
#             cause_dict = json.loads(cause_resp.get("content").decode('utf-8'))
#             # Preparing custom error response list
#             error["status"] = cause_dict.get("error").get("status", None)
#             error["code"] = cause_dict.get("error").get("code", None)
#             error["error_code"] = cause_dict.get("error").get("details")[0].get('errorCode', None)
#             error["cause"] = cause_dict.get("error").get("message", None)
#             errors_lst.append(error)

#     resp = Response(
#         success_count=batch_response.success_count,
#         message=f"sent message to {batch_response.success_count} device(s)",
#         error=ErrorResponse(
#             count=batch_response.failure_count,
#             errors=errors_lst
#         )
#     )

#     return resp