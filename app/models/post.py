from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from typing import  List, Optional, Dict
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



# Get only my post
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