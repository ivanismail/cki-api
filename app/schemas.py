from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time
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

class ShiftBase(BaseModel):
    name: str
    start_time: time
    end_time: time
    late_tolerance: int = 0

class ShiftCreate(ShiftBase):
    pass

class Shift(ShiftBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class AttendanceBase(BaseModel):
    user_id: int
    shift_id: int

class AttendanceCreate(AttendanceBase):
    pass

class Attendance(AttendanceBase):
    id: int
    check_in: datetime
    check_out: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True