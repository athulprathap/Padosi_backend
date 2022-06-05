from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
import models
from database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()
 

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

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

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return{"status":"success"}

@app.get("/getAll")
async def get_all(db: Session = Depends(get_db)):
    # post = cursor.execute("""SELECT * FROM posts""")
    # post = cursor.fetchall()
    allPost = db.query(models.Post).all()
    return {'info': allPost }


@app.post("/create", status_code=status.HTTP_201_CREATED)
async def create_post(post:Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # newPost = cursor.fetchone()
    # conn.commit()
    
    newPost = models.Post(**post.dict())  #Note: '**post.dict' is a substitude for writing list of schema properties such post.title ,post.content etc

    db.add(newPost)
    db.commit()
    db.refresh(newPost)

    return {"info":newPost}


@app.get("/getOne/{id}")
async def get_post(id:int, db:Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=post)
    
    singlePost = db.query(models.Post).filter(models.Post.id == id).first()

    if not singlePost:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=post)

    return {"info":singlePost}



@app.delete("/delete/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_Post(id:int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),))
    # deletedPost = cursor.fetchone()
    # conn.commit()
    
    deletePost = db.query(models.Post).filter(models.Post.id == id).first()
    if not deletePost:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post id:{id} does not exist!")

        deletePost.delete(synchronize_session=False)
        db.commit()
    
    return Response(status_code = status.HTTP_204_NO_CONTENT)



@app.put("/edit/{id}")
def editPost(id:int, update_post:Post, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (str(id))))

    # editedPost = cursor.fetchone()
    # conn.commit()
    editedPost = db.query(models.Post).filter(models.Post.id == id)

    post = editedPost.first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, datail=f"post with id:{id} does not exist!")

    editedPost.update(update_post.dict(), synchronize_session=False)
    db.commit()

    return {"data": editedPost.first()}