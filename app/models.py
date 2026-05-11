from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger, Enum, Time, Date, Numeric, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base
import datetime
import enum

class RoleEnum(enum.Enum):
    admin = "admin"
    employee = "employee"

class AttendanceStatus(enum.Enum):
    present = "present"
    late = "late"
    absent = "absent"
    leave = "leave"

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    name = Column(String(100), index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    role = Column(Enum(RoleEnum), default=RoleEnum.employee)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    attendances = relationship("Attendance", back_populates="user")
    user_shifts = relationship("UserShift", back_populates="user")

class Shift(Base):
    __tablename__ = "shifts"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    name = Column(String(50))
    start_time = Column(Time)
    end_time = Column(Time)
    late_tolerance = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user_shifts = relationship("UserShift", back_populates="shift")

class UserShift(Base):
    __tablename__ = "user_shifts"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), index=True)
    shift_id = Column(BigInteger, ForeignKey("shifts.id"), index=True)
    start_date = Column(Date)
    end_date = Column(Date)

    user = relationship("User", back_populates="user_shifts")
    shift = relationship("Shift", back_populates="user_shifts")

class Attendance(Base):
    __tablename__ = "attendances"
    __table_args__ = (
        UniqueConstraint('user_id', 'date', name='unique_attendance'),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), index=True)
    date = Column(Date, index=True)
    check_in = Column(DateTime, nullable=True)
    check_out = Column(DateTime, nullable=True)
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.present)
    check_in_lat = Column(Numeric(10, 6), nullable=True)
    check_in_lng = Column(Numeric(10, 6), nullable=True)
    check_out_lat = Column(Numeric(10, 6), nullable=True)
    check_out_lng = Column(Numeric(10, 6), nullable=True)
    check_in_photo = Column(String(255), nullable=True)
    check_out_photo = Column(String(255), nullable=True)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="attendances")