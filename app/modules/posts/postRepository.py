from fastapi import FastAPI, Response, requests, status, HTTPException, Depends 
from ...model import personal_post, create, singlePost, allPost, update, delete
from ...pydantic_schemas.posts import Post
from typing import  Dict
from sqlalchemy.orm import Session
from ...import oauth2
from ...database import get_db


def create_post(post:Post, db: Session,  user:int= Depends(oauth2.get_current_user)):
    return create(db=db, post=post, user=user)


def myPost(post:Post, db: Session, user:int = Depends(oauth2.get_current_user)):
    return personal_post(db=db, post=post, user=user)

def get_all_post(db: Session, user:int = Depends(oauth2.get_current_user)):
    return allPost(db=db)


# def reactions(db: Session, like:Likes, user:int=Depends(oauth2.get_current_user)):
    
#     actions = like_unlike(like=like, db=db, user=user)
    
#     if (like.dir == 1):
#         if actions:
#             raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= f"You have already liked this post!")
#         newLike = Like(post_id = like.post_id, user_id = account_owner.id)
#         db.add(newLike)
#         db.commit()
#         return {"msg": "You Liked this Post!"}
#     else: 
#         if not actions:
#             raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"Like not found!")
         
#         query_like.delete()
#         db.commit()
        
        
#         return ({"msg": "You unliked this post"}, actions)

def single_Post(db: Session, id: int):
    post = singlePost(id=id, db=db)
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"User not found!")
    
    return post


def updatePost(id:int, post:Post, user:int, db: Session, values: Dict={}):
    
    editpost =  update(id=id, post=post, db=db, values=values)

    if not editpost :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, datail=f"post with id:{id} does not exist!")
    
    elif editpost.user_id != user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"You can't perform this action!")
    
    return editpost 


