from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import SessionLocal
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/send", response_model=schemas.InviteOut)
def send_invite(invite: schemas.InviteCreate, db: Session = Depends(get_db)):
    return crud.create_invite(db, invite)

@router.post("/{invite_id}/respond", response_model=schemas.InviteOut)
def respond_to_invite(invite_id: int, status: str, db: Session = Depends(get_db)):
    updated = crud.update_invite_status(db, invite_id, status)
    if not updated:
        return {"error": "Invite not found"}
    return updated


@router.get("/user/{user_id}", response_model=List[schemas.InviteOut])
def get_user_invites(user_id: int, db: Session = Depends(get_db)):
    return crud.get_invites_for_user(db, user_id)
    
