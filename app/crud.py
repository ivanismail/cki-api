from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash, verify_password
import datetime

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

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

def create_attendance_log(db: Session, log: schemas.AttendanceLogCreate):
    db_log = models.AttendanceLog(
        user_id=log.user_id,
        action=log.action,
        time=log.time,
        lat=log.lat,
        lng=log.lng,
        device_info=log.device_info
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_attendance_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AttendanceLog).offset(skip).limit(limit).all()

def get_attendance_logs_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.AttendanceLog).filter(models.AttendanceLog.user_id == user_id).offset(skip).limit(limit).all()

def get_attendance_log(db: Session, log_id: int):
    return db.query(models.AttendanceLog).filter(models.AttendanceLog.id == log_id).first()

def create_leave_request(db: Session, leave: schemas.LeaveRequestCreate):
    db_leave = models.LeaveRequest(
        user_id=leave.user_id,
        start_date=leave.start_date,
        end_date=leave.end_date,
        type=leave.type,
        reason=leave.reason
    )
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave

def get_leave_request(db: Session, request_id: int):
    return db.query(models.LeaveRequest).filter(models.LeaveRequest.id == request_id).first()

def get_leave_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.LeaveRequest).offset(skip).limit(limit).all()

def get_leave_requests_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.LeaveRequest).filter(models.LeaveRequest.user_id == user_id).offset(skip).limit(limit).all()

def approve_leave_request(db: Session, request_id: int, approved_by: int):
    db_leave = db.query(models.LeaveRequest).filter(models.LeaveRequest.id == request_id).first()
    if db_leave:
        db_leave.status = models.LeaveRequestStatus.approved
        db_leave.approved_by = approved_by
        db.commit()
        db.refresh(db_leave)
    return db_leave

def reject_leave_request(db: Session, request_id: int):
    db_leave = db.query(models.LeaveRequest).filter(models.LeaveRequest.id == request_id).first()
    if db_leave:
        db_leave.status = models.LeaveRequestStatus.rejected
        db.commit()
        db.refresh(db_leave)
    return db_leave

def delete_leave_request(db: Session, request_id: int):
    db_leave = db.query(models.LeaveRequest).filter(models.LeaveRequest.id == request_id).first()
    if db_leave:
        db.delete(db_leave)
        db.commit()
    return db_leave