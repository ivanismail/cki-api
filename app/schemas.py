from pydantic import BaseModel
from typing import Optional, Generic, TypeVar
from datetime import datetime, time, date
from enum import Enum
from decimal import Decimal

T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    success: bool = True
    message: Optional[str] = None
    data: Optional[T] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RoleEnum(str, Enum):
    admin = "admin"
    employee = "employee"

class AttendanceStatus(str, Enum):
    present = "present"
    late = "late"
    absent = "absent"
    leave = "leave"

class AttendanceLogAction(str, Enum):
    check_in = "check_in"
    check_out = "check_out"

class LeaveRequestType(str, Enum):
    sick = "sick"
    leave = "leave"
    permission = "permission"

class LeaveRequestStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

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

class UserShiftBase(BaseModel):
    user_id: int
    shift_id: int
    start_date: date
    end_date: date

class UserShiftCreate(UserShiftBase):
    pass

class UserShift(UserShiftBase):
    id: int

    class Config:
        orm_mode = True

class AttendanceBase(BaseModel):
    user_id: int
    date: date
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    status: AttendanceStatus = AttendanceStatus.present
    check_in_lat: Optional[Decimal] = None
    check_in_lng: Optional[Decimal] = None
    check_out_lat: Optional[Decimal] = None
    check_out_lng: Optional[Decimal] = None
    check_in_photo: Optional[str] = None
    check_out_photo: Optional[str] = None
    note: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    pass

class Attendance(AttendanceBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class AttendanceLogBase(BaseModel):
    user_id: int
    action: AttendanceLogAction
    time: datetime
    lat: Optional[Decimal] = None
    lng: Optional[Decimal] = None
    device_info: Optional[str] = None

class AttendanceLogCreate(AttendanceLogBase):
    pass

class AttendanceLog(AttendanceLogBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class CheckInRequest(BaseModel):
    lat: Optional[Decimal] = None
    lng: Optional[Decimal] = None
    photo: Optional[str] = None
    device_info: Optional[str] = None

class CheckOutRequest(BaseModel):
    lat: Optional[Decimal] = None
    lng: Optional[Decimal] = None
    photo: Optional[str] = None
    device_info: Optional[str] = None

class LeaveRequestBase(BaseModel):
    user_id: int
    start_date: date
    end_date: date
    type: LeaveRequestType
    reason: str
    status: LeaveRequestStatus = LeaveRequestStatus.pending
    approved_by: Optional[int] = None

class LeaveRequestCreate(BaseModel):
    user_id: int
    start_date: date
    end_date: date
    type: LeaveRequestType
    reason: str

class LeaveRequest(LeaveRequestBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True