from typing import  List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models, schema, oauth2
from database import  get_db

router = APIRouter(tags = ['Posts'])


@router.get("/ownerPost", response_model=List[schema.PostOpt])
async def get_owner_post(db: Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):

    owner_post = db.query(models.Post).filter(models.Post.user_id == account_owner.id).all()
    return   owner_post


@router.get("/allPosts", response_model=List[schema.PostOpt])
async def get_allPost(db: Session = Depends(get_db), limit:int = 6, skip:int = 0, search: Optional[str] = "", account_owner: int = Depends(oauth2.get_current_user)):
    allPost = db.query(models.Post).filter(models.Post.title.contains(search)).all()
    
    return allPost[limit+skip]
    

@router.post("/create", status_code=status.HTTP_201_CREATED,  response_model=schema.PostOpt)
async def create_post(post:schema.CreatePost, db: Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):

# "user_id = current_user.id" identifies the owner of a post created by its id....
    newPost = models.Post(user_id = account_owner.id, **post.dict())  
    db.add(newPost)
    db.commit()
    db.refresh(newPost)

    return newPost


@router.get("/getOne/{id}",  response_model=schema.PostOpt)
async def get_post(id:int, db:Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):

    singlePost = db.query(models.Post).filter(models.Post.id == id).first()

    if not singlePost:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"User not found!")

    return singlePost


@router.delete("/delete/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_Post(id: int, db: Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):

    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    
    post = deleted_post.first()
 

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post id:{id} does not exist!")

    elif post.user_id != account_owner.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"You can't perform this action!")

    deleted_post.delete()
    db.commit()
    
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@router.put("/edit/{id}",  response_model=schema.PostOpt)
async def editPost(id:int, update_post:schema.CreatePost, db: Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):

    editedPost = db.query(models.Post).filter(models.Post.id == id)
    
    post =  editedPost.first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, datail=f"post with id:{id} does not exist!")
    
    elif post.user_id != account_owner.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"You can't perform this action!")

    editedPost.update(update_post.dict())
    db.commit()

    return  editedPost.first()