from typing import  List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models, schema, oauth2
from database import  get_db

router = APIRouter(tags = ['Posts'])


@router.get("/getAll", response_model=List[schema.PostOpt])
async def get_all(db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):

    allPost = db.query(models.Post).all()
    return  allPost 


@router.post("/create", status_code=status.HTTP_201_CREATED,  response_model=schema.PostOpt)
async def create_post(post:schema.CreatePost, db: Session = Depends(get_db), get_current_user:int = Depends(oauth2.get_current_user)):

    newPost = models.Post(**post.dict())  
    db.add(newPost)
    db.commit()
    db.refresh(newPost)

    return newPost


@router.get("/getOne/{id}",  response_model=schema.PostOpt)
async def get_post(id:int, db:Session = Depends(get_db), get_current_user:int = Depends(oauth2.get_current_user)):

    singlePost = db.query(models.Post).filter(models.Post.id == id).first()

    if not singlePost:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"User not found!")

    return singlePost


@router.delete("/delete/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_Post(id:int, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):

    deletePost = db.query(models.Post).filter(models.Post.id == id).first()

    if not deletePost:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post id:{id} does not exist!")

        deletePost.delete(synchronize_session=False)
        db.commit()
    
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@router.put("/edit/{id}",  response_model=schema.PostOpt)
async def editPost(id:int, update_post:schema.CreatePost, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):

    editedPost = db.query(models.Post).filter(models.Post.id == id)
    post = editedPost.first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, datail=f"post with id:{id} does not exist!")

    editedPost.update(update_post.dict(), synchronize_session=False)
    db.commit()

    return  editedPost.first()