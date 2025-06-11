from sqlalchemy.orm import Session
from app import models, schemas

# CRUD - create, read, update, and delete operations
# Create new entries in the database (e.g. add a new player)

# Read data from the database (e.g. get a list of all events)

# Update records (e.g. change someone's skill level)

# Delete records (e.g. remove a cancelled event)

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_event(db: Session, event: schemas.EventCreate):
    positions_csv = ",".join(event.required_positions)
    db_event = models.Event(
        title=event.title,
        location=event.location,
        event_time=event.event_time,
        required_positions=positions_csv,
        creator_id=event.creator_id,
        is_public=event.is_public
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    # Convert string to list if needed
    if isinstance(db_event.required_positions, str):
        db_event.required_positions = db_event.required_positions.split(",")

    return db_event

def create_invite(db: Session, invite: schemas.InviteCreate):
    db_invite = models.Invite(**invite.dict())
    db.add(db_invite)
    db.commit()
    db.refresh(db_invite)
    return db_invite

def update_invite_status(db: Session, invite_id: int, status: str):
    invite = db.query(models.Invite).filter(models.Invite.id == invite_id).first()
    if invite:
        invite.status = status
        db.commit()
        db.refresh(invite)
    return invite

def get_invites_for_user(db: Session, user_id: int):
    return db.query(models.Invite).filter(models.Invite.invited_user_id == user_id).all()

def update_invite_status(db: Session, invite_id: int, status: str):
    invite = db.query(models.Invite).filter(models.Invite.id == invite_id).first()
    if not invite:
        return None
    invite.status = status
    db.commit()
    db.refresh(invite)
    return invite


