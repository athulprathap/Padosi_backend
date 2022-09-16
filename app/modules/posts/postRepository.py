from fastapi import FastAPI, Response, requests, status, HTTPException, Depends 
from ...model import personal_post, create, singlePost, allPost, update, delete, like_unlike, Like
from ...pydantic_schemas.posts import Post
from typing import  Dict
from sqlalchemy.orm import Session
from ...import oauth2
from ...database import get_db


def create_post(post:Post, db: Session,  user:int= Depends(oauth2.get_current_user)):
    return create(post=post, db=db, user=user)

def myPost(db: Session, user: int = Depends(oauth2.get_current_user)):
    return personal_post(db=db, user=user)

def get_all_post(db: Session, user: int = Depends(oauth2.get_current_user)):
    return allPost(db=db)


def reactions(db: Session, like:Like, user:int=Depends(oauth2.get_current_user)):
    
    isLiked  = like_unlike(like=like, db=db, user=user)
    
    if (like.dir == 1):
        if isLiked :
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= f"You have already liked this post!")
        newLike = Like(post_id = like.post_id, user_id = user.id)
        db.add(newLike)
        db.commit()
        
        return {"msg": "You Liked this Post!"}
    else: 
        if not isLiked :
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"Like not found!")
        
        return ({"msg": "You unliked this post"})


def single_Post(db: Session, id: int):
    post = singlePost(id=id, db=db)
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post not found!")
    
    return post


def updatePost(id:int, post:Post, user:int, db: Session, values: Dict={}):
    
    editpost =  update(id=id, post=post, db=db, values=values)

    if not editpost:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist!")
    
    elif editpost.user_id != user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"You can't perform this action!")
    
    return editpost 


def delete_post(id: int, db: Session,  user : int = Depends(oauth2.get_current_user)):
    
    destroy = delete(id=id, user=user, db=db)
    
    if not destroy:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post id:{id} does not exist!")

    elif destroy.user_id != user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"You can't perform this action!")
    
    return destroy


