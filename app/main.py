from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
import models, schema
from database import engine, Base, get_db

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


def post_by_Id(id):
    for p in myPost:
        if p['id'] == id:
         return p

@app.get("/getAll")
async def get_all(db: Session = Depends(get_db)):
    allPost = db.query(models.Post).all()
    return {'info': allPost }


@app.post("/create", status_code=status.HTTP_201_CREATED)
async def create_post(post:schema.Post, db: Session = Depends(get_db)):
    newPost = models.Post(**post.dict())  #Note: '**post.dict' is a substitude for writing list of schema properties such post.title ,post.content etc
    db.add(newPost)
    db.commit()
    db.refresh(newPost)

    return {"info":newPost}


@app.get("/getOne/{id}")
async def get_post(id:int, db:Session = Depends(get_db)):
    singlePost = db.query(models.Post).filter(models.Post.id == id).first()
    if not singlePost:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=post)

    return {"info":singlePost}


@app.delete("/delete/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_Post(id:int, db: Session = Depends(get_db)):
    deletePost = db.query(models.Post).filter(models.Post.id == id).first()
    if not deletePost:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post id:{id} does not exist!")

        deletePost.delete(synchronize_session=False)
        db.commit()
    
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put("/edit/{id}")
def editPost(id:int, update_post:schema.Post, db: Session = Depends(get_db)):
    editedPost = db.query(models.Post).filter(models.Post.id == id)
    post = editedPost.first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, datail=f"post with id:{id} does not exist!")

    editedPost.update(update_post.dict(), synchronize_session=False)
    db.commit()

    return {"data": editedPost.first()}