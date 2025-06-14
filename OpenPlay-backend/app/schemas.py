from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime, timezone
from typing import List
import pytz

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
    city: Optional[str]
    state: Optional[str]

class UserUpdate(BaseModel):
    phone: Optional[str]
    gender: Optional[str]
    skill_level: Optional[str]
    preferred_position_1: Optional[str]
    preferred_position_2: Optional[str]
    city: Optional[str]
    state: Optional[str]

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
    event_time: str
    timezone: str    # e.g. "America/New_York"
    required_positions: List[str]
    creator_id: int
    is_public: Optional[str] = "true"
    description: Optional[str] = None

    @validator("event_time")
    def parse_event_time(cls, v):
        try:
            return datetime.strptime(v, "%Y-%m-%d %I:%M %p")  # 12-hour format
        except ValueError:
            raise ValueError("Invalid time format. Use 'YYYY-MM-DD HH:MM AM/PM'")
    
    @validator("timezone")
    def validate_timezone(cls, v):
        if v not in pytz.all_timezones:
            raise ValueError("Invalid timezone string")
        return v

    def to_utc(self):
        if isinstance(self.event_time, str):
            naive_time = datetime.strptime(self.event_time, "%Y-%m-%d %I:%M %p")
        else:
            naive_time = self.event_time
        return naive_time.astimezone(timezone.utc)
    
class EventUpdate(BaseModel):
    title: Optional[str]
    location: Optional[str]
    event_time: Optional[str]
    required_positions: Optional[List[str]]
    is_public: Optional[str]
    description: Optional[str] = None

    @validator("event_time")
    def parse_event_time(cls, v):
        try:
            return datetime.strptime(v, "%Y-%m-%d %I:%M %p")
        except ValueError:
            raise ValueError("Invalid time format. Use 'YYYY-MM-DD HH:MM AM/PM'")

class EventOut(BaseModel):
    id: int
    title: str
    location: str
    event_time: datetime
    required_positions: List[str]
    creator_id: int
    is_public: str
    description: Optional[str] = None
    timezone: str

    class Config:
        orm_mode = True
        from_attributes = True
    
    @staticmethod
    def from_orm_with_local(obj):
        local = pytz.timezone(obj.timezone)
        local_time = obj.event_time.astimezone(local)
        data = obj.__dict__.copy()
        data["event_time"] = local_time.strftime("%Y-%m-%d %I:%M %p")
        return EventOut(**data)

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
