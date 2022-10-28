from enum import unique
import json
from .models.user import create_user, update_user, singleUser,Address,deactivate_user,Vote
from .models.post import create, singlePost, delete, update, allPost, Like, personal_post, like_unlike,Post
from .models.otp import find_otp_block,find_otp_life_time,save_otp,save_otp_failed_count,save_block_otp,disable_otp
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Numeric, DateTime
from sqlalchemy.orm import relationship
from .database import Base
import datetime
from sqlalchemy.sql.sqltypes import TIMESTAMP, DATE
from sqlalchemy.sql.expression import text

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    content = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"))
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"))
    com_owner = relationship("User")
    com_post = relationship("Post")
    
class BaseModel:
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False,
        server_default=text("now()"), onupdate=datetime.datetime.now)
    is_deleted = Column(Boolean, server_default="FALSE", nullable=False)

class DeviceToken(Base,BaseModel):
    __tablename__ = "device_tokens"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    token = Column(String, nullable=False)
    is_enable = Column(Boolean, server_default="TRUE", nullable=True)
    message_preview = Column(Boolean, server_default= "TRUE", nullable= True)



# class user_devices(Base,BaseModel):
#     __tablename__ = "user_devices"

#     id = Column(Integer, primary_key=True, nullable=False, index=True)
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
#     token = Column(String(255),unique=True, nullable=False)
#     device_info = Column(json, nullable=True)

class Event(Base):
    __tablename__ = "Events"

    id = Column(Integer, primary_key=True)
    content = Column(String)
    description = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"))
    area = Column(String, nullable=False)
    region = Column(String, nullable=False)
    pincode = Column(Integer, nullable=False)
    event_dateandtime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    is_deleted = Column(Boolean, server_default="FALSE", nullable=False)

class EventRespond(Base):
    __tablename__ = 'EventRespond'

    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    event_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)