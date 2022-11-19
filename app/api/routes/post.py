from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..modules.postRepository import create_post, myPost, get_all_post, single_Post, updatePost, delete_post, reactions
from ..schema import Post, PostAll, PostOpt, CreatePost, Likes
from typing import  List
from app.api import model,schema
from sqlalchemy.orm import Session
from  ..database import get_db
from  ..oauth2 import get_current_user,get_current_active_user


router = APIRouter(tags = ['Posts'])


@router.get("/ownerPost")
async def get_owner_post(db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    return myPost(db=db, user=user)



@router.get("/allPosts", response_model=List[PostAll])
async def get_allPost(db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    return get_all_post(db=db, user=user)
    
    

@router.post("/create", status_code=status.HTTP_201_CREATED,  response_model=PostOpt)
async def createPost(post:Post, db: Session = Depends(get_db), user:int= Depends(get_current_user)):
    return create_post(db=db, post=post, user=user)
    


@router.post("/like", status_code= status.HTTP_201_CREATED)
async def like_post(like: Likes, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    return reactions(db=db, like=like, user=user)

    

@router.get("/getOne/{id}")
async def get_singlepost(id:int, db:Session = Depends(get_db), user: int = Depends(get_current_user)):
    return single_Post(id=id, db=db)



@router.delete("/delete/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_Post(id: int, db: Session = Depends(get_db), user: int = Depends(get_current_user)):    
    return delete_post(id=id, db=db, user=user)



@router.put("/edit/{id}",  response_model=PostOpt)
async def editPost(id:int, post:CreatePost, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    return updatePost(id=id, post=post, user=user, db=db, values=dict(post))

@router.post("/report_post")
def report_post(report_post: schema.Reportpost, db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)):

    report = model.ReportPosts(post_id=report_post.post_id, reported_by=current_user.id, message=report_post.message,count= +1)

    db.add(report)
    db.commit()
    db.refresh(report)
    
    if not report:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Please try again")

    return report