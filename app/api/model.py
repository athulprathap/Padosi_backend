from email.policy import default
from enum import unique
import json
from typing import Sequence
from requests import session
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Numeric, DateTime,Sequence,ARRAY
from sqlalchemy.orm import relationship
from .database import Base
import datetime
from sqlalchemy.sql.sqltypes import TIMESTAMP, DATE
from sqlalchemy.sql.expression import text

class BaseModel:
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False,
        server_default=text("now()"), onupdate=datetime.datetime.now)
    is_deleted = Column(Boolean, server_default="FALSE", nullable=False)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    is_admin = Column(Boolean, server_default="FALSE", nullable=False)
    password = Column(String, nullable=False)
    is_deleted = Column(Boolean, server_default="FALSE", nullable=False)
    # passcode = Column(String, nullable=True)  # used for forgot user
    # passcode_expiry_time = Column(TIMESTAMP(timezone=True), nullable=True)
    # image = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
class Address(Base):
    __tablename__ = 'address' 
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    housenumber: String = Column(String)
    apartment: String = Column(String)
    city: String = Column(String)
    area: String = Column(String)
    pincode: Integer = Column(Integer)
    state: String=Column(String)
    latitude = Column(Numeric, nullable=True)
    longitude = Column(Numeric, nullable=True)
    user: relationship('User', back_populates='address')

class BlockUser(Base):
    __tablename__ = "block_users"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    blocked_user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    blocker_user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

class urgent_alerts(Base):
    __tablename__ = "urgent_alerts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")
    
class respond_to_alerts(Base):
    __tablename__="response"
    id=Column(Integer, ForeignKey("urgent_alerts.id", ondelete="CASCADE"),primary_key=True)
    respond=Column(String, nullable=False)


class UserRecommadation(Base):
    __tablename__ = "user_recommmandations"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    self_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    status = Column(
        String,
        Enum("L", "U", "PENDING", "MAYBE", name="status"),
        nullable=False,
        default="PENDING",
    )

class ReportUser(Base, BaseModel):
    __tablename__ = "report_users"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    reported_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    reported_to = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    message = Column(String, nullable=False)
    viewed = Column(Boolean, server_default="FALSE", nullable=False)

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)

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


class otps(Base):
    __tablename__= "otps"
    
    id = Column(Integer,Sequence("otp_id_seq"),primary_key=True)
    recipient_id = Column(String)
    session_id = Column(String)
    otp_code = Column(String)
    status = Column(String)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    otp_failed_count = Column(Integer,default=0)

class otpblocks(Base):
    __tablename__= "otp_blocks"
    id = Column(Integer,Sequence("otp_block_id_seq"),primary_key=True)
    recipient_id = Column(String)
    created_on = Column(DateTime)
    
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
    __tablename__ = "events"

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
    is_private = Column(Boolean, server_default = "False",nullable = False)
    is_public = Column(Boolean, server_default = "True",nullable = False)
    event_dateandtime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    is_deleted = Column(Boolean, server_default="FALSE", nullable=False)

class EventRespond(Base):
    __tablename__ = 'eventrespond'

    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    event_id = Column(Integer, ForeignKey(
        "events.id", ondelete="CASCADE"), primary_key=True)

class Search(Base):
    __tablename__= 'search'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"))
    recent_search = Column((String), nullable=True)

class Popular_search(Base):
    __tablename__= 'popular_search'
    id = Column(Integer, primary_key=True, nullable=False)
    Popular_search = Column((String),nullable=True)

