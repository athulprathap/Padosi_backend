from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from typing import  List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from ..import oauth2
from ..pydantic_schemas.posts import Post, CreatePost, Likes, PostOpt
from ..models.user import User
from ..database import get_db, Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")
    
class Like(Base):
    __tablename__ = "likes"
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)



def personal_post(db: Session, user_id: int = 0):
    owner_post = db.query(Post).filter(Post.user_id == user_id).all()
    return  owner_post


# def create(post:schema.CreatePost, db: Session, account_owner: int = Depends(oauth2.get_current_user)):
# # "user_id = current_user.id" identifies the owner of a post created by its id....
#     newPost = Post(user_id = account_owner.id, **post.dict())  
#     db.add(newPost)
#     db.commit()
#     db.refresh(newPost)

#     return newPost

def create(post:Post, db: Session, user: str):
    newPost = Post( title=post.title, content=post.content, published=post.published, user=user)
    
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    
    return newPost


def allPost(db: Session = Depends(get_db), limit:int = 4, skip:int = 0, option: Optional[str] = "",
                                             account_owner: int = Depends(oauth2.get_current_user)):
    # join tables and get the results
    allPost  = db.query(Post, func.count(Like.post_id).label("likes")).join(Like, Like.post_id == Post.id,
            isouter=True).group_by(Post.id).filter(Post.title.contains(option)).limit(limit).offset(skip).all()
        
    return allPost 


def like_unlike(like: Likes, db: Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):
    
    query_like = db.query(Like).filter(Like.post_id == like.post_id, Like.user_id == account_owner.id)
    
    isLiked = query_like.first()
    
    if (like.dir == 1):
        if isLiked:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= f"You have already liked this post!")
        newLike = Like(post_id = like.post_id, user_id = account_owner.id)
        db.add(newLike)
        db.commit()
        return {"msg": "You Liked this Post!"}
    else: 
        if not isLiked:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"Like not found!")
         
        query_like.delete()
        db.commit()
        
        return {"msg": "You unliked this post"}


def singlePost(id:int, db:Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):
    single_post = db.query(Post, func.count(Like.post_id).label("likes")).join(Like,
                 Like.post_id == Post.id, isouter=True).group_by(Post.id).filter(Post.id == id).first()

    if not single_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"User not found!")

    return single_post
    

# Delete a Post
def delete(id: int, db: Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):

    deleted_post = db.query(Post).filter(Post.id == id)
    
    post = deleted_post.first()
 
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post id:{id} does not exist!")

    elif post.user_id != account_owner.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"You can't perform this action!")

    deleted_post.delete()
    db.commit()
    
    return Response(status_code = status.HTTP_204_NO_CONTENT)


# Edit/Update a Post
def update(id:int, update_post:CreatePost, db: Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):

    editedPost = db.query(Post).filter(Post.id == id)
    
    post =  editedPost.first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, datail=f"post with id:{id} does not exist!")
    
    elif post.user_id != account_owner.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"You can't perform this action!")

    editedPost.update(update_post.dict())
    db.commit()

    return  editedPost.first()