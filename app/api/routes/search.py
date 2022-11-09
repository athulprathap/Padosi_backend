from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import model, schema, database
from ..oauth2 import get_current_user


# creates the router for the events endpoints
router = APIRouter(
    prefix="/search",
    tags=["search"]
)

@router.post("/recent_search", status_code=status.HTTP_201_CREATED)
def recent_search(search:schema.Search, db: Session = Depends(database.get_db), current_user: int = Depends(get_current_user)):
    search = model.Search(user_id=current_user.id,recent_search=search.recent_search)

    db.add(search)
    db.commit()
    db.refresh(search)

    return search

@router.get("/me")
def get_search_by_me(db: Session = Depends(database.get_db), current_user: int = Depends(get_current_user)):
    search = db.query(model.Search).filter(model.Search.user_id == current_user.id).order_by(model.Search.id.desc()).limit(10).all()
    if not search:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No search to show")
    return {"results":search}

@router.post("/popular_search")
def popular_search(search:schema.Search, db: Session = Depends(database.get_db)):
    popular=model.Popular_search(Popular_search=search.recent_search)
    db.add(popular)
    db.commit()
    db.refresh(popular)

    return popular

# @router.get("/popular_searches")
# def get_search_by_me(db: Session = Depends(database.get_db), current_user: int = Depends(get_current_user)):
#     popular = db.query(model.Popular_search).filter(model.Popular_search.Popular_search).count(max).all()
#     if not popular:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"No search to show")
#     return {"results":popular}