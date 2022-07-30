from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from typing import  List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .. import  oauth2
from ..import schema, utils
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


# Get post Created only by owner
async def get_owner_post(db: Session, account_owner: int = Depends(oauth2.get_current_user)):
    owner_post = db.query(models.Post).filter(models.Post.user_id == account_owner.id).all()
    return   owner_post


# Create a Post
def create(post:schema.CreatePost, db: Session, account_owner: int = Depends(oauth2.get_current_user)):

# "user_id = current_user.id" identifies the owner of a post created by its id....
    newPost = Post(user_id = account_owner.id, **post.dict())  
    db.add(newPost)
    db.commit()
    db.refresh(newPost)

    return newPost


# Get all Post
async def get_allPost(db: Session = Depends(get_db), limit:int = 6, skip:int = 0, option: Optional[str] = "", account_owner: int = Depends(oauth2.get_current_user)):
    
    # allPost = db.query(models.Post).filter(models.Post.title.contains(option)).limit(limit).offset(skip).all()
    
    # join tables and get the results
    allPost  = db.query(models.Post, func.count(models.Like.post_id).label("likes")).join(models.Like, models.Like.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(option)).limit(limit).offset(skip).all()
        
    
    return allPost 