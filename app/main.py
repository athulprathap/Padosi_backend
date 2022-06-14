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

<<<<<<< HEAD

@app.get("/getAll", response_model=schema.ReturnedFields)
async def get_all(db: Session = Depends(get_db)):
    allPost = db.query(models.Post).all()
    return  allPost 


@app.post("/create", status_code=status.HTTP_201_CREATED,  response_model=schema.ReturnedFields)
async def create_post(post:schema.CreatePost, db: Session = Depends(get_db)):
    newPost = models.Post(**post.dict())  #Note: '**post.dict' is a substitude for writing list of schema properties such post.title ,post.content etc
    db.add(newPost)
    db.commit()
    db.refresh(newPost)

    return newPost


@app.get("/getOne/{id}",  response_model=schema.ReturnedFields)
async def get_post(id:int, db:Session = Depends(get_db)):
    singlePost = db.query(models.Post).filter(models.Post.id == id).first()
    if not singlePost:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=post)

    return singlePost


@app.delete("/delete/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_Post(id:int, db: Session = Depends(get_db)):
    deletePost = db.query(models.Post).filter(models.Post.id == id).first()
    if not deletePost:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post id:{id} does not exist!")

        deletePost.delete(synchronize_session=False)
        db.commit()
    
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put("/edit/{id}",  response_model=schema.ReturnedFields)
def editPost(id:int, update_post:schema.CreatePost, db: Session = Depends(get_db)):
    editedPost = db.query(models.Post).filter(models.Post.id == id)
    post = editedPost.first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, datail=f"post with id:{id} does not exist!")

    editedPost.update(update_post.dict(), synchronize_session=False)
    db.commit()

    return  editedPost.first()
=======
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
>>>>>>> 5243f632015ecf3749147a8edbeb28badce479b7
