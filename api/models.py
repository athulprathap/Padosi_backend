from argparse import ONE_OR_MORE
from curses import meta
import datetime
from email.mime import base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, Table, Float, Enum, Numeric, MetaData, Integer, Sequence

metadata = MetaData()

users = Table(
    'my_users', metadata,
    Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
    Column('email', String(100)),
    Column('password', String(100)),
    Column('fullname', String(50)),
    Column('created_on', DateTime),
    Column('status', String(1)),
)

base = Table(
    'base', metadata,
    Column('is_deleted', Boolean),
    Column('created_on', DateTime(), default=func.now()),
    Column('updated_on', DateTime(), default=func.now(), onupdate=func.now()),
    Column('created_by', String(50)),
    Column('updated_by', String(50)),
)

codes = Table(
    'codes', metadata,
    Column('id', Integer, Sequence('code_id_seq'), primary_key=True),
    Column('email', String(100)),
    Column('reset_code', String(50)),
    Column('expired_in', DateTime),
    Column('status', String(1))
)

class Base():
    __tablename__ = 'base', metadata , 

    is_delete: bool = False
    created_by: Column(ForeignKey('users.id'), nullable=True)
    updated_by: Column(ForeignKey('users.id'), nullable=True)
    created_at: DateTime = Column(DateTime, default=datetime)
    updated_at: DateTime = Column(DateTime, default=datetime)


class UserProfile(Base):
    __tablename__ = 'user_profile' , metadata,

    first_name: String = Column(String)
    last_name: String = Column(String)
    email: String = Column(String)
    phone: String = Column(String)
    
    profile_picture: String = Column(String) 
    cover_picture: String = Column(String) 

    gender: Enum = Column(Enum)
    followers: Integer = Column(Integer)
    following: Integer = Column(Integer)
    about: String = Column(String)
    is_private: bool = False

    address: String = Column(String)
    about: String = Column(String)
    birthday: DateTime = Column(DateTime)

    user: relationship('User', back_populates='profile')


class User(UserProfile):
    __tablename__ = 'users', metadata , 

    id: Integer = Column(Integer, primary_key=True)
    username: String = Column(String)
    password: String = Column(String)
    email: String = Column(String)
    is_admin: bool = Column(Boolean)
    is_active: bool = Column(Boolean)
    is_delete: bool = Column(Boolean)


class Address(Base):
    __tablename__ = 'address' , metadata ,

    housenumber: String = Column(String)
    apartment: String = Column(String)
    city: String = Column(String)
    area: String = Column(String)
    pincode: Integer = Column(Integer)
    state: Enum = Column(Enum)
    user: relationship('User', back_populates='address')


class Following(Base):
    __tablename__ = 'following', metadata,

    following_by: Column(ForeignKey('users.id'), primary_key=True)
    following_to: Column(ForeignKey('users.id'), primary_key=True)
    follow_accept: bool = Column(Boolean)

    user: relationship('User', back_populates='following')
    following: relationship('User', back_populates='followers')


class Post(Base):
    __tablename__ = 'posts', metadata ,

    message: String = Column(String)
    number_of_likes: Integer = Column(Integer)
    location: String = Column(String)
    post_image: String = Column(String)
    post_type: Enum = Column(Enum) # image, video, text, audio
    comments: relationship(ONE_OR_MORE)
    user_profile: relationship('UserProfile', back_populates='post')
    post_reports: relationship('PostReport', back_populates='post')


class PostLikes(Base):
    __tablename__ = 'post_likes', metadata,

    liked_by: Column(ForeignKey('users.id'), primary_key=True)
    post: Column(ForeignKey('posts.id'), primary_key=True)
    liked_at: DateTime = Column(DateTime, default=datetime)


class PostComments(Base):
    __tablename__ = 'post_comments' , metadata ,

    commented_by: Column(ForeignKey('users.id'), primary_key=True)
    post: Column(ForeignKey('posts.id'), primary_key=True)


class CommentLikes(Base):
    __tablename__ = 'comment_likes' , metadata ,

    liked_by: Column(ForeignKey('users.id'), primary_key=True)
    comment: Column(ForeignKey('post_comments.id'), primary_key=True)


