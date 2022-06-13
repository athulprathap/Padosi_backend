from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from routes import post, user, auth

Base.metadata.create_all(bind=engine)

app = FastAPI()
 

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapiblog',user='postgres', password='shongokeye', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connected successfully!')
        break
    except Exception as error:
        print('Database connection failed!')
        print('error: ',  error)
        time.sleep(4)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)