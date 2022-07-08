from argparse import ONE_OR_MORE
import datetime
from email.mime import base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Table, PrimaryKeyConstraint, Float, Enum, Numeric


class Base():
    __tablename__ = 'base'

    is_delete: bool = False
    created_by: (ForeignKey('users.id'), nullable=True)
    updated_by: (ForeignKey('users.id'), nullable=True)
    created_at: DateTime = Column(DateTime, default=datetime.now)
    updated_at: DateTime = Column(DateTime, default=datetime.now)


class UserProfile(Base):
    __tablename__ = 'user_profile'

    first_name: String = Column(String)
    last_name: String = Column(String)
    email: String = Column(String)
    phone: String = Column(String)
    
    profile_picture: String = Column(String) 
    cover_picture: String = Column(String) 

    gender: Enum = Column(Enum)
    followers: int = Column(int)
    follwing: int = Column(int)
    about: String = Column(String)
    is_private: bool = False

    address: String = Column(String)
    about: String = Column(String)
    birthday: DateTime = Column(DateTime)

    user: relationship('User', back_populates='profile')


class User(UserProfile):
    __tablename__ = 'users'

    id: Integer = Column(Integer, primary_key=True)
    username: String = Column(String)
    password: String = Column(String)
    is_admin: bool = Column(Boolean)
    is_active: bool = Column(Boolean)
    is_delete: bool = Column(Boolean)


class Address(Base):
    __tablename__ = 'address'

    housenumber: String = Column(String)
    apartment: String = Column(String)
    city: String = Column(String)
    area: String = Column(String)
    pincode: int = Column(int)
    state: Enum = Column(Enum)
    user: relationship('User', back_populates='address')


class Following(Base):
    __tablename__ = 'following'

    following_by: Column(ForeignKey('users.id'), primary_key=True)
    following_to: Column(ForeignKey('users.id'), primary_key=True)
    follow_accept: bool = Column(Boolean)

    __table_args__ = (PrimaryKeyConstraint('user', 'following'),)

    user: relationship('User', back_populates='following')
    following: relationship('User', back_populates='followers')


class Post(Base):
    __tablename__ = 'posts'

    message: String = Column(String)
    number_of_likes: int = Column(int)
    location: String = Column(String)
    post_image: String = Column(String)
    post_type: Enum = Column(Enum) # image, video, text, audio
    comments: relationship(ONE_OR_MORE)
    user_profile: relationship('UserProfile', back_populates='post')
    post_reports: relationship('PostReport', back_populates='post')


class PostLikes(Base):
    __tablename__ = 'post_likes'

    liked_by: Column(ForeignKey('users.id'), primary_key=True)
    post: Column(ForeignKey('posts.id'), primary_key=True)
    liked_at: DateTime = Column(DateTime, default=datetime.now)


class PostComments(Base):
    __tablename__ = 'post_comments'

    commented_by: Column(ForeignKey('users.id'), primary_key=True)
    post: Column(ForeignKey('posts.id'), primary_key=True)


class CommentLikes(Base):
    __tablename__ = 'comment_likes'

    liked_by: Column(ForeignKey('users.id'), primary_key=True)
    comment: Column(ForeignKey('post_comments.id'), primary_key=True)


