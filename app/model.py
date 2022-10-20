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

class BaseModel:
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False,
        server_default=text("now()"), onupdate=datetime.datetime.now)
    is_deleted = Column(Boolean, server_default="FALSE", nullable=False)

class DeviceToken(Base, BaseModel):
    __tablename__ = "device_tokens"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    token = Column(String, nullable=False)
    is_enable = Column(Boolean, server_default="TRUE", nullable=True)
    message_preview = Column(Boolean, server_default= "TRUE", nullable= True)



class user_devices(Base, BaseModel):
    __tablename__ = "user_devices"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    token = Column(String(255),unique=True, nullable=False)
    device_info = Column(json, nullable=True)

