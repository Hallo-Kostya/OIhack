from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel

class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

class EmployeeResponse(BaseModel):
    id: int
    crm_id: int
    name: str
    position: Optional[str] = None
    department: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        from_attributes = True