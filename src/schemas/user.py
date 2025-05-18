from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from src.models.user import WorkStatus

class UserBase(BaseModel):
    full_name: str
    birth_date: datetime
    position: str
    department: str
    work_status: WorkStatus
    email: EmailStr
    phone: Optional[str] = None
    profile_photo: Optional[str] = None
    about: Optional[str] = None
    hobbies: Optional[str] = None
    skills: Optional[str] = None
    preferences: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    birth_date: Optional[datetime] = None
    position: Optional[str] = None
    department: Optional[str] = None
    work_status: Optional[WorkStatus] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    profile_photo: Optional[str] = None
    about: Optional[str] = None
    hobbies: Optional[str] = None
    skills: Optional[str] = None
    preferences: Optional[str] = None

class UserInDB(UserBase):
    id: int

    class Config:
        from_attributes = True 