from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from src.models.user import WorkStatus

class UserBase(BaseModel):
    first_name: str
    last_name: str
    birth_date: datetime
    project: str
    department: str
    email: EmailStr
    phone: Optional[str] = None
    profile_photo: Optional[str] = None
    about: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[datetime] = None
    project: Optional[str] = None
    department: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    profile_photo: Optional[str] = None
    about: Optional[str] = None

class UserInDB(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: datetime
    department: str
    project: str
    email: EmailStr
    phone: Optional[str] = None
    profile_photo: Optional[str] = None
    about: Optional[str] = None

    class Config:
        from_attributes = True 