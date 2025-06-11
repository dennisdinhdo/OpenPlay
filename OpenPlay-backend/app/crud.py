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

def update_event(db: Session, event_id: int, data: schemas.EventUpdate, requester_id: int):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        return None, "Event not found"
    if event.creator_id != requester_id:
        return None, "Unauthorized"
    
    for key, value in data.dict(exclude_unset=True).items():
        if key == "required_positions":
            setattr(event, key, ",".join(value)) # this will convert list to string
        else:
            setattr(event, key, value)

    db.commit()
    db.refresh(event)
    return event, None

def delete_event(db: Session, event_id: int, requester_id: int):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        return None, "event not found"
    if event.creator_id != requester_id:
        return None, "Not authorized"
    
    db.delete(event)
    db.commit()
    return True, None

def create_invite(db: Session, invite: schemas.InviteCreate):
    db_invite = models.EventInvite(**invite.dict())
    db.add(db_invite)
    db.commit()
    db.refresh(db_invite)
    return db_invite

def delete_event_invite(db: Session, invite_id: int, requester_id: int):
    invite = db.query(models.EventInvite).filter(models.EventInvite.id == invite_id).first()

    if not invite:
        return None, "Invite not found"

    event = db.query(models.Event).filter(models.Event.id == invite.event_id).first()
    if not event:
        return None, "Associated event not found"

    if event.creator_id != requester_id:
        return None, "Unauthorized: Only the event creator can uninvite users"

    db.delete(invite)
    db.commit()
    return True, None


def update_invite_status(db: Session, invite_id: int, status: str):
    invite = db.query(models.EventInvite).filter(models.EventInvite.id == invite_id).first()
    if invite:
        invite.status = status
        db.commit()
        db.refresh(invite)
    return invite

def get_invites_for_user(db: Session, user_id: int):
    return db.query(models.EventInvite).filter(models.EventInvite.invited_user_id == user_id).all()


