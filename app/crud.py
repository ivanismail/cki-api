from sqlalchemy.orm import Session
from . import models, schemas
import datetime

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_shift(db: Session, shift_id: int):
    return db.query(models.Shift).filter(models.Shift.id == shift_id).first()

def get_shifts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Shift).offset(skip).limit(limit).all()

def create_shift(db: Session, shift: schemas.ShiftCreate):
    db_shift = models.Shift(
        name=shift.name,
        start_time=shift.start_time,
        end_time=shift.end_time,
        late_tolerance=shift.late_tolerance
    )
    db.add(db_shift)
    db.commit()
    db.refresh(db_shift)
    return db_shift

def get_attendances(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Attendance).offset(skip).limit(limit).all()

def create_attendance(db: Session, attendance: schemas.AttendanceCreate):
    db_attendance = models.Attendance(
        user_id=attendance.user_id,
        shift_id=attendance.shift_id
    )
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def update_attendance_check_out(db: Session, attendance_id: int):
    db_attendance = db.query(models.Attendance).filter(models.Attendance.id == attendance_id).first()
    if db_attendance:
        db_attendance.check_out = datetime.datetime.utcnow()
        db.commit()
        db.refresh(db_attendance)
    return db_attendance