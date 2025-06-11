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

    # If private, only the creator or invited people can view
    if event.is_public != "true":
        is_creator = event.creator_id == user_id
        is_invited = db.query(models.Invite).filter(
            models.Invite.event_id == event_id,
            models.Invite.invited_user_id == user_id
        ).first()
        if not (is_creator or is_invited):
            return {"error": "Unauthorized: This event is private"}

    invites = db.query(models.Invite).filter(models.Invite.event_id == event_id).all()
    roster = []
    for i in invites:
        user = db.query(models.User).filter(models.User.id == i.invited_user_id).first()
        roster.append({
            "user_id": user.id,
            "username": user.username,
            "position": i.position,
            "status": i.status
        })

    return {
        "event_id": event.id,
        "event_title": event.title,
        "roster": roster
    }
