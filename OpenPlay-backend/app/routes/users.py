from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@router.put("/{user_id}/update", response_model=schemas.UserOut)
def update_user(user_id: int, updates: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user, error = crud.update_user_profile(db, user_id, updates)
    if not updated_user:
        return {"error": error}
    return updated_user
