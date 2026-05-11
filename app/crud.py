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

def create_user_shift(db: Session, user_shift: schemas.UserShiftCreate):
    db_user_shift = models.UserShift(
        user_id=user_shift.user_id,
        shift_id=user_shift.shift_id,
        start_date=user_shift.start_date,
        end_date=user_shift.end_date
    )
    db.add(db_user_shift)
    db.commit()
    db.refresh(db_user_shift)
    return db_user_shift

def get_user_shift(db: Session, user_shift_id: int):
    return db.query(models.UserShift).filter(models.UserShift.id == user_shift_id).first()

def get_user_shifts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UserShift).offset(skip).limit(limit).all()

def get_user_shifts_by_user(db: Session, user_id: int):
    return db.query(models.UserShift).filter(models.UserShift.user_id == user_id).all()

def get_user_shifts_by_shift(db: Session, shift_id: int):
    return db.query(models.UserShift).filter(models.UserShift.shift_id == shift_id).all()

def delete_user_shift(db: Session, user_shift_id: int):
    db_user_shift = db.query(models.UserShift).filter(models.UserShift.id == user_shift_id).first()
    if db_user_shift:
        db.delete(db_user_shift)
        db.commit()
    return db_user_shift

def get_attendances(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Attendance).offset(skip).limit(limit).all()

def create_attendance(db: Session, attendance: schemas.AttendanceCreate):
    db_attendance = models.Attendance(
        user_id=attendance.user_id,
        date=attendance.date,
        check_in=attendance.check_in,
        check_out=attendance.check_out,
        status=attendance.status,
        check_in_lat=attendance.check_in_lat,
        check_in_lng=attendance.check_in_lng,
        check_out_lat=attendance.check_out_lat,
        check_out_lng=attendance.check_out_lng,
        check_in_photo=attendance.check_in_photo,
        check_out_photo=attendance.check_out_photo,
        note=attendance.note
    )
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def update_attendance_check_out(db: Session, attendance_id: int, check_out_lat: float = None, check_out_lng: float = None, check_out_photo: str = None):
    db_attendance = db.query(models.Attendance).filter(models.Attendance.id == attendance_id).first()
    if db_attendance:
        db_attendance.check_out = datetime.datetime.utcnow()
        if check_out_lat:
            db_attendance.check_out_lat = check_out_lat
        if check_out_lng:
            db_attendance.check_out_lng = check_out_lng
        if check_out_photo:
            db_attendance.check_out_photo = check_out_photo
        db.commit()
        db.refresh(db_attendance)
    return db_attendance

def get_attendance_by_user_date(db: Session, user_id: int, date_val: datetime.date):
    return db.query(models.Attendance).filter(
        models.Attendance.user_id == user_id,
        models.Attendance.date == date_val
    ).first()