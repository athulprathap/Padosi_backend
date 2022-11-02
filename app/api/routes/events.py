from asyncio import events
from multiprocessing import Event
from turtle import title
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import model, schema, database
from ..oauth2 import get_current_user


# creates the router for the events endpoints
router = APIRouter(
    prefix="/events",
    tags=["events"]
)
@router.get("/", response_model=List[schema.Events])
def get_Events(db: Session = Depends(database.get_db), current_user: int = Depends(get_current_user)):
    events = db.query(model.Event).filter(model.Event.is_public == True).all()
    return events


@router.post("/create_events", status_code=status.HTTP_201_CREATED)
def create_event(event: schema.Events, db: Session = Depends(database.get_db), current_user: int = Depends(get_current_user)):

    new_event = model.Event(user_id=current_user.id,content=event.content,description=event.description,
    area=event.area,region=event.region,pincode=event.pincode,is_private=event.is_private)

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event

@router.get("/me", response_model=List[schema.Events])
def get_Events_by_me(db: Session = Depends(database.get_db), current_user: int = Depends(get_current_user)):

    events = db.query(model.Event).filter(model.Event.user_id == current_user.id).all()
    if not events:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No events to show")
    return events

@router.get("/event/id")
def get_Events_by_id(id, db: Session = Depends(database.get_db)):

    events = db.query(model.Event).filter(model.Event.id == id).first()
    if not events:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"event with id: {id} was not found")
    return events
    

@router.delete("/delete_events", status_code=status.HTTP_200_OK)
def delete_event(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(get_current_user)):

    event_query = db.query(model.Event).filter(
        model.Event.id == id)
    event_ = event_query.first()

    if event_ == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"event with id: {id} does not exist")
    elif event_.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=" Not authorized to perfrom rquested action")

    event_query.delete(synchronize_session=False)
    db.commit()

    return ("deleted Successfully")

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schema.Events)
def update_post(id, post: schema.Events, db: Session = Depends(database.get_db), current_user: int = Depends(get_current_user)):

    event_query = db.query(model.Event).filter(
        model.Event.id == id).update()
    event_ = event_query.first()

    if event_ == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"event with id: {id} does not exist")
    elif event_.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=" Not authorized to perfrom rquested action")

    db.commit()

    return event_query.first()

@router.post("/respond/id", status_code=status.HTTP_201_CREATED)
def event_respond(EventRespond: schema.EventRespond, db: Session = Depends(database.get_db), current_user: int = Depends(get_current_user)):

    event = db.query(model.Event).filter(model.Event.id == EventRespond.event_id).first()

    if not event: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'event with id: {EventRespond.event_id} does not exist')
    event_query = db.query(model.EventRespond).filter(
        model.EventRespond.user_id == current_user.id, model.EventRespond.event_id == EventRespond.event_id)

    event_found = event_query.first()

    if (EventRespond.dir == 1):
        if event_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'User with id:{current_user.id} already going in event with id:{EventRespond.event_id}')
        going = model.EventRespond(user_id=current_user.id, event_id=EventRespond.event_id)
        db.add(going)
        db.commit()
        return{"message": "going"}

   
    elif (EventRespond.dir == 0):
        if not event_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'User with id:{current_user.id} is intrested with id:{EventRespond.event_id}')
        event_query.delete(synchronize_session=False)
        db.commit()
        return{"message": "intrested"}

    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Invalid like direction it should be 1 or 0')