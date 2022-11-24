from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import model, schema
from  ..oauth2 import get_current_user
from ..database import get_db


router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/create_polls",status_code=status.HTTP_201_CREATED)
def create_polls(pol: schema.Addpolls,db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    new = model.polls(content = pol.content, option1 = pol.option1, option2 = pol.option2,
    option3 = pol.option3, option4 = pol.option4, option6 = pol.option6, user_id = current_user.id)
    if current_user.id:
        db.add(new)
        db.commit()
        db.refresh(new)
        return("polls create successfully")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schema.Vote,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):

    post = db.query(model.polls).filter(model.polls.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Polls with id :{vote.post_id} does not exist",
        )

    vote_query = db.query(model.Vote).filter(
        model.Vote.post_id == vote.post_id, model.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with id:{current_user.id} has already voted on post {vote.post_id}",
            )
        new_vote = model.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "vote casted"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vote not found",
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "vote deleted"}
