from fastapi import FastAPI, Response, requests, status, HTTPException, Depends 
from ...model import personal_post, create, singlePost, allPost, update, delete
from ...pydantic_schemas.posts import Post, PostOpt
from sqlalchemy.orm import Session
from ...import oauth2
from ...database import get_db
from typing import Dict


def create_post(post:Post, db: Session,  user: str):
    return create(db=db, post=post, user=user)
   