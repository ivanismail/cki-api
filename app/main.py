from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Attendance API", description="API for attendance system")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to Attendance API"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.post("/shifts/", response_model=schemas.Shift)
def create_shift(shift: schemas.ShiftCreate, db: Session = Depends(get_db)):
    return crud.create_shift(db=db, shift=shift)

@app.get("/shifts/", response_model=List[schemas.Shift])
def read_shifts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    shifts = crud.get_shifts(db, skip=skip, limit=limit)
    return shifts

@app.get("/shifts/{shift_id}", response_model=schemas.Shift)
def read_shift(shift_id: int, db: Session = Depends(get_db)):
    shift = crud.get_shift(db, shift_id=shift_id)
    return shift

@app.post("/user_shifts/", response_model=schemas.UserShift)
def create_user_shift(user_shift: schemas.UserShiftCreate, db: Session = Depends(get_db)):
    return crud.create_user_shift(db=db, user_shift=user_shift)

@app.get("/user_shifts/", response_model=List[schemas.UserShift])
def read_user_shifts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_shifts = crud.get_user_shifts(db, skip=skip, limit=limit)
    return user_shifts

@app.get("/user_shifts/user/{user_id}", response_model=List[schemas.UserShift])
def read_user_shifts_by_user(user_id: int, db: Session = Depends(get_db)):
    user_shifts = crud.get_user_shifts_by_user(db, user_id=user_id)
    return user_shifts

@app.get("/user_shifts/shift/{shift_id}", response_model=List[schemas.UserShift])
def read_user_shifts_by_shift(shift_id: int, db: Session = Depends(get_db)):
    user_shifts = crud.get_user_shifts_by_shift(db, shift_id=shift_id)
    return user_shifts

@app.delete("/user_shifts/{user_shift_id}")
def delete_user_shift(user_shift_id: int, db: Session = Depends(get_db)):
    return crud.delete_user_shift(db=db, user_shift_id=user_shift_id)

@app.post("/attendances/", response_model=schemas.Attendance)
def create_attendance(attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    return crud.create_attendance(db=db, attendance=attendance)

@app.put("/attendances/{attendance_id}/check_out", response_model=schemas.Attendance)
def check_out(attendance_id: int, check_out_lat: float = None, check_out_lng: float = None, check_out_photo: str = None, db: Session = Depends(get_db)):
    return crud.update_attendance_check_out(db=db, attendance_id=attendance_id, check_out_lat=check_out_lat, check_out_lng=check_out_lng, check_out_photo=check_out_photo)

@app.get("/attendances/", response_model=List[schemas.Attendance])
def read_attendances(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    attendances = crud.get_attendances(db, skip=skip, limit=limit)
    return attendances

@app.get("/attendances/{user_id}/{date}", response_model=schemas.Attendance)
def read_attendance_by_user_date(user_id: int, date: str, db: Session = Depends(get_db)):
    from datetime import datetime as dt
    attendance_date = dt.strptime(date, "%Y-%m-%d").date()
    return crud.get_attendance_by_user_date(db, user_id=user_id, date_val=attendance_date)

@app.post("/attendance_logs/", response_model=schemas.AttendanceLog)
def create_attendance_log(log: schemas.AttendanceLogCreate, db: Session = Depends(get_db)):
    return crud.create_attendance_log(db=db, log=log)

@app.get("/attendance_logs/", response_model=List[schemas.AttendanceLog])
def read_attendance_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = crud.get_attendance_logs(db, skip=skip, limit=limit)
    return logs

@app.get("/attendance_logs/user/{user_id}", response_model=List[schemas.AttendanceLog])
def read_attendance_logs_by_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = crud.get_attendance_logs_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return logs

@app.get("/attendance_logs/{log_id}", response_model=schemas.AttendanceLog)
def read_attendance_log(log_id: int, db: Session = Depends(get_db)):
    return crud.get_attendance_log(db, log_id=log_id)

@app.post("/leave_requests/", response_model=schemas.LeaveRequest)
def create_leave_request(leave: schemas.LeaveRequestCreate, db: Session = Depends(get_db)):
    return crud.create_leave_request(db=db, leave=leave)

@app.get("/leave_requests/", response_model=List[schemas.LeaveRequest])
def read_leave_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    requests = crud.get_leave_requests(db, skip=skip, limit=limit)
    return requests

@app.get("/leave_requests/user/{user_id}", response_model=List[schemas.LeaveRequest])
def read_leave_requests_by_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    requests = crud.get_leave_requests_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return requests

@app.get("/leave_requests/{request_id}", response_model=schemas.LeaveRequest)
def read_leave_request(request_id: int, db: Session = Depends(get_db)):
    return crud.get_leave_request(db, request_id=request_id)

@app.put("/leave_requests/{request_id}/approve", response_model=schemas.LeaveRequest)
def approve_leave_request(request_id: int, approved_by: int, db: Session = Depends(get_db)):
    return crud.approve_leave_request(db=db, request_id=request_id, approved_by=approved_by)

@app.put("/leave_requests/{request_id}/reject", response_model=schemas.LeaveRequest)
def reject_leave_request(request_id: int, db: Session = Depends(get_db)):
    return crud.reject_leave_request(db=db, request_id=request_id)

@app.delete("/leave_requests/{request_id}")
def delete_leave_request(request_id: int, db: Session = Depends(get_db)):
    return crud.delete_leave_request(db=db, request_id=request_id)