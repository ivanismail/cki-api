from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger, Enum, Time
from sqlalchemy.orm import relationship
from .database import Base
import datetime
import enum

class RoleEnum(enum.Enum):
    admin = "admin"
    employee = "employee"

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    name = Column(String(100), index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    role = Column(Enum(RoleEnum), default=RoleEnum.employee)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    attendances = relationship("Attendance", back_populates="user")

class Shift(Base):
    __tablename__ = "shifts"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    name = Column(String(50))
    start_time = Column(Time)
    end_time = Column(Time)
    late_tolerance = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    attendances = relationship("Attendance", back_populates="shift")

class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), index=True)
    shift_id = Column(BigInteger, ForeignKey("shifts.id"), index=True)
    check_in = Column(DateTime, default=datetime.datetime.utcnow)
    check_out = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="attendances")
    shift = relationship("Shift", back_populates="attendances")