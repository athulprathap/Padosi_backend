from email.policy import default
from enum import unique
import json
from typing import Sequence, List
from requests import session
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Numeric, DateTime,Sequence,ARRAY,JSON
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

class User(Base,BaseModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String,unique = True,nullable=True)
    email = Column(String, unique=True, nullable=False)
    is_admin = Column(Boolean, server_default="FALSE", nullable=False)
    password = Column(String, nullable=False)
    passcode = Column(String, nullable=True)  # used for forgot user
    passcode_expiry_time = Column(TIMESTAMP(timezone=True), nullable=True)
    status = Column(String, Enum("ACTIVE", "SUSPEND", "DELETED",
            name="user_status",), nullable=False, default="ACTIVE")
    is_blocked = Column(Boolean, server_default="FALSE", nullable=False)
    mobile = Column(String, nullable=False)
    # passcode = Column(String, nullable=True)  # used for forgot user
    # passcode_expiry_time = Column(TIMESTAMP(timezone=True), nullable=True)
    # image = Column(String, nullable=False)
    profile = relationship("UserProfile", back_populates="user")
    
class Address(Base):
    __tablename__ = 'address' 
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    housenumber = Column(String)
    apartment = Column(String)
    city = Column(String)
    area = Column(String)
    pincode = Column(Integer, nullable=False)
    state = Column(String)
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

class ReportUser(Base, BaseModel):
    __tablename__ = "report_users"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    reported_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    reported_to = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    message = Column(String, nullable=False)

class ReportPosts(Base, BaseModel):
    __tablename__ = "report_posts"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    reported_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    message = Column(String, nullable=False)
    count = Column(Integer,nullable=True)
    status = Column(String, Enum("Pending","Rejected","Resolved", name = "status"),nullable = False, default="Pending")

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    poll_id = Column(Integer, ForeignKey("polls.id",ondelete="CASCADE"),primary_key=True)

class UserProfile(Base, BaseModel):
    __tablename__ = "userprofiles"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    full_name = Column(String, nullable=False)
    mobile = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    sex = Column(String, nullable=True)
    date_of_birth = Column(DATE, nullable=True)
    # bio = Column(String, nullable=True)
    # birth_star = Column(String, nullable=True)
    # education = Column(String, nullable=True)
    # height = Column(Numeric, nullable=True)
    # profession = Column(String, nullable=True)
    # athnicity = Column(String, nullable=True)
    # intension = Column(String, nullable=True)
    # smoker = Column(Boolean, nullable=True)
    # drink = Column(Boolean, nullable=True)
    # marital_status = Column(String, Enum("Single","Divorced","Separated", "Annulled","Widowed",
    #     name="marital_status"), server_default="Single", nullable=True)
    # no_of_children = Column(Integer, nullable=True)
    age = Column(Integer, nullable=True)
    # profile_complete_percent = Column(Numeric, nullable=True)
    # latitude = Column(Numeric, nullable=True)
    # longitude = Column(Numeric, nullable=True)
    # address = Column(String, nullable=True)
    # is_verified = Column(Boolean, server_default="FALSE", nullable=False)
    # selfie_verification = Column(Boolean, server_default="FALSE", nullable=False)
    # selfie_image_url = Column(String, nullable=True)
    name_change_date = Column(TIMESTAMP(timezone=True), nullable=False,
        server_default=text("now()"))
    # is_hide_profile = Column(Boolean, server_default="FALSE", nullable=False)
    user = relationship("User", back_populates="profile")

class Post(Base,BaseModel):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=True)
    content = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")

class Image(Base, BaseModel):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    image_url = Column(String, nullable=False)
    
class Like(Base,BaseModel):
    __tablename__ = "likes"
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)


class Comment(Base,BaseModel):
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



class user_devices(Base,BaseModel):
    __tablename__ = "user_devices"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    token = Column(String(255),unique=True, nullable=False)
    device_info = Column(JSON, nullable=True)

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
    counter = Column(Integer)
    id = Column(Integer, primary_key=True, nullable=False)
    Popular_search = Column((String),nullable=True)

class ChangeAddress(Base):
    __tablename__ = 'changeaddress'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"))
    message = Column(String,nullable=True)
    status = Column(String, Enum("Pending","Rejected","Resolved", name = "status"),nullable = False, default="Pending")
    change_city = Column(String,nullable = False)
    change_area = Column(String, nullable = False)
    allowance = Column(Boolean, server_default="FALSE", nullable=False)

# class AdminPermision(Base):
#     __tablename__ = "admin_permision"
#     id = Column(Integer, primary_key=True, nullable=False)
#     user_id = Column(Integer, ForeignKey(
#         "users.id", ondelete="CASCADE"))
#     change_id = Column(Integer, ForeignKey(
#         "changeaddress.id", ondelete="CASCADE"))
#     allowance = Column(Boolean, server_default="FALSE", nullable=False)

class polls(Base):
    __tablename__ = "polls"
    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String)
    user_id = Column(Integer, ForeignKey(
         "users.id", ondelete="CASCADE"),nullable = False)
    option1=Column(String,nullable=True)
    option2=Column(String,nullable=True)
    option3=Column(String,nullable=True)
    option4=Column(String,nullable=True)
    option6=Column(String,nullable=True)

class Question(Base):
    __tablename__ = "question"
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer, ForeignKey(
         "users.id", ondelete="CASCADE"),nullable = False)
    choice_text = Column(String(200))
    question_text = Column(String(200))
    pub_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    choices = relationship('Choice', back_populates="question")
# class Question(Base):
# 	__tablename__ = "question"
# 	id = Column(Integer, primary_key=True)
# 	question_text = Column(String(200))
# 	pub_date = Column(DateTime)
    
    
# 	choices = relationship('Choice', back_populates="question")


class Choice(Base):
	__tablename__ = "choice"
	id = Column(Integer, primary_key=True)
	question_id = Column(Integer, ForeignKey('question.id', ondelete='CASCADE'))
	choice_text = Column(String(200))
	votes = Column(Integer, default=0)

	question = relationship("Question", back_populates="choices")