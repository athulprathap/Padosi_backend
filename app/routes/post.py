from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..modules.posts.postRepository import create_post, myPost, get_all_post, single_Post, updatePost, delete_post
from ..pydantic_schemas.posts import Post, PostAll, PostOpt, CreatePost
from typing import  List
from sqlalchemy.orm import Session
from  ..database import get_db
from ..import oauth2


router = APIRouter(tags = ['Posts'])


# Get post Created only by owner
@router.get("/ownerPost", response_model=List[PostAll])
async def get_owner_post(db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    return myPost(db=db,  user=user)


# Get all Post
@router.get("/allPosts", response_model=List[PostAll])
async def get_allPost( db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    return get_all_post(db=db, user=user)
    
    
# Create a Post
@router.post("/create", status_code=status.HTTP_201_CREATED,  response_model=PostOpt)
async def createPost(post:Post, db: Session = Depends(get_db), user:int= Depends(oauth2.get_current_user)):
    return create_post(db=db, post=post, user=user)
    

# # # Like & Unlike Post
# @router.post("/like", status_code= status.HTTP_201_CREATED)
# async def like_post(like: Like, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
#     return reactions(db=db, like=like, user=user)

    
# # Get a Post
@router.get("/getOne/{id}")
async def get_singlepost(id:int, db:Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    return single_Post(id=id, db=db)


# Delete a Post
@router.delete("/delete/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_Post(id: int, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):    
    return delete_post(id=id, db=db, user=user)


# Edit/Update a Post
@router.put("/edit/{id}",  response_model=PostOpt)
async def editPost(id:int, post:CreatePost, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    return updatePost(id=id, post=post, user=user, db=db, values=dict(post))