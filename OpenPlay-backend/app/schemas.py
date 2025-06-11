from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from typing import List

# Shape of the data. blue print of the data. the object? 
# Validates incoming data (request)
# control what daata you send back (response)
# auto generate api docs


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    phone: Optional[str]
    gender: Optional[str]
    skill_level: Optional[str]
    preferred_position_1: Optional[str]
    preferred_position_2: Optional[str]

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone: Optional[str]
    gender: Optional[str]
    skill_level: Optional[str]
    preferred_position_1: Optional[str]
    preferred_position_2: Optional[str]

    class Config:
        orm_mode = True

class EventCreate(BaseModel):
    title: str
    location: str
    event_time: datetime
    required_positions: List[str]
    creator_id: int
    is_public: Optional[str] = "true"
    description: Optional[str] = None
    
class EventUpdate(BaseModel):
    title: Optional[str]
    location: Optional[str]
    event_time: Optional[datetime]
    required_positions: Optional[List[str]]
    is_public: Optional[str]
    description: Optional[str] = None

class EventOut(BaseModel):
    id: int
    title: str
    location: str
    event_time: datetime
    required_positions: List[str]
    creator_id: int
    is_public: str
    description: Optional[str] = None

    class Config:
        orm_mode = True

class InviteCreate(BaseModel):
    event_id: int
    invited_user_id: int
    position: str

class InviteOut(BaseModel):
    id: int
    event_id: int
    invited_user_id: int
    position: str
    status: str

    class Config:
        orm_mode = True
