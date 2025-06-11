from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal
from typing import List
from app import models


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=schemas.EventOut)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db, event)

@router.get("/all", response_model=List[schemas.EventOut])
def get_all_events(db: Session = Depends(get_db)):
    events = db.query(models.Event).all()
    for e in events:
        e.required_positions = e.required_positions.split(",") if e.required_positions else []
    return events

@router.get("/{event_id}/roster")
def get_event_roster(event_id: int, user_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        return {"error": "Event not found"}

    # Authorization for private events
    if event.is_public != "true":
        is_creator = event.creator_id == user_id
        is_invited = db.query(models.EventInvite).filter(
            models.EventInvite.event_id == event_id,
            models.EventInvite.invited_user_id == user_id
        ).first()
        if not (is_creator or is_invited):
            return {"error": "Unauthorized: This event is private"}

    invites = db.query(models.EventInvite).filter(models.EventInvite.event_id == event_id).all()
    roster = []
    for i in invites:
        user = db.query(models.User).filter(models.User.id == i.invited_user_id).first()
        roster.append({
            "user_id": user.id,
            "username": user.username,
            "position": i.position,
            "status": i.status  # <-- this now reflects accepted/rejected/pending
        })

    return {
        "event_id": event.id,
        "event_title": event.title,
        "roster": roster
    }

@router.put("/{event_id}/update")
def update_event(event_id: int, data: schemas.EventUpdate, requester_id: int, db: Session = Depends(get_db)):
    updated_event, error = crud.update_event(db, event_id, data, requester_id)
    if not updated_event:
        return {"error": error}
    return updated_event

@router.delete("/{event_id}/delete")
def delete_event(event_id: int, requester_id: int, db: Session = Depends(get_db)):
    success, error = crud.delete_event(db, event_id, requester_id)
    if not success:
        return {"error": error}
    return {"message": "Event deleted successfully"}
