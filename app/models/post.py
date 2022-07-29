from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .. import  oauth2
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