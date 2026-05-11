from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    employee = "employee"

class UserBase(BaseModel):
    name: str
    email: str
    password: str
    role: RoleEnum = RoleEnum.employee

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class AttendanceBase(BaseModel):
    user_id: int

class AttendanceCreate(AttendanceBase):
    pass

class Attendance(AttendanceBase):
    id: int
    check_in: datetime
    check_out: Optional[datetime]

    class Config:
        orm_mode = True