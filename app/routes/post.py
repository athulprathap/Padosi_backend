from typing import  List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schema, oauth2
from database import  get_db

router = APIRouter(tags = ['Posts'])

# Get post Created only by owner
@router.get("/ownerPost", response_model=List[schema.PostOpt])
async def get_owner_post(db: Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):

    owner_post = db.query(models.Post).filter(models.Post.user_id == account_owner.id).all()
    return   owner_post

# Get all Post
@router.get("/allPosts", response_model=List[schema.PostAll])
async def get_allPost(db: Session = Depends(get_db), limit:int = 6, skip:int = 0, option: Optional[str] = "", account_owner: int = Depends(oauth2.get_current_user)):
    
    # allPost = db.query(models.Post).filter(models.Post.title.contains(option)).limit(limit).offset(skip).all()
    
    
    # join tables and get the results
    allPost  = db.query(models.Post, func.count(models.Like.post_id).label("likes")).join(models.Like, models.Like.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(option)).limit(limit).offset(skip).all()
        
    
    return allPost 
    
# Create a Post
@router.post("/create", status_code=status.HTTP_201_CREATED,  response_model=schema.PostOpt)
async def create_post(post:schema.CreatePost, db: Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):

# "user_id = current_user.id" identifies the owner of a post created by its id....
    newPost = models.Post(user_id = account_owner.id, **post.dict())  
    db.add(newPost)
    db.commit()
    db.refresh(newPost)

    return newPost


# Like & Unlike Post
@router.post("/like", status_code= status.HTTP_201_CREATED)
async def like_post(like: schema.Likes, db: Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):
    
    query_like = db.query(models.Like).filter(models.Like.post_id == like.post_id, models.Like.user_id == account_owner.id)
    
    isLiked = query_like.first()
    
    if (like.dir == 1):
        if isLiked:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= f"You have already liked this post!")
        newLike = models.Like(post_id = like.post_id, user_id = account_owner.id)
        db.add(newLike)
        db.commit()
        return {"msg": "You Liked this Post!"}
    else: 
        if not isLiked:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"Like not found!")
         
        query_like.delete()
        db.commit()
        
        return {"msg": "You unliked this post"}
    
    
# Get a Post
@router.get("/getOne/{id}",  response_model=schema.PostOpt)
async def get_post(id:int, db:Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):

    # singlePost = db.query(models.Post).filter(models.Post.id == id).first()
    
    singlePost = db.query(models.Post, func.count(models.Like.post_id).label("likes")).join(models.Like, models.Like.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not singlePost:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"User not found!")

    return singlePost

# Delete a Post
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

# Edit/Update a Post
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