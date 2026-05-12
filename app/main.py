from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas, auth, exception
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Attendance API", description="API for attendance system")

app.add_exception_handler(HTTPException, exception.http_exception_handler)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return schemas.BaseResponse(message="Welcome to Attendance API")

@app.post("/token", response_model=schemas.BaseResponse[schemas.TokenResponse])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return schemas.BaseResponse(data=schemas.TokenResponse(access_token=access_token))

@app.get("/users/me", response_model=schemas.BaseResponse[schemas.User])
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return schemas.BaseResponse(data=current_user)

@app.post("/users/", response_model=schemas.BaseResponse[schemas.User])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return schemas.BaseResponse(data=crud.create_user(db=db, user=user))

@app.get("/users/", response_model=schemas.BaseResponse[List[schemas.User]])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return schemas.BaseResponse(data=users)

@app.post("/shifts/", response_model=schemas.BaseResponse[schemas.Shift])
def create_shift(shift: schemas.ShiftCreate, db: Session = Depends(get_db)):
    return schemas.BaseResponse(data=crud.create_shift(db=db, shift=shift))

@app.get("/shifts/", response_model=schemas.BaseResponse[List[schemas.Shift]])
def read_shifts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    shifts = crud.get_shifts(db, skip=skip, limit=limit)
    return schemas.BaseResponse(data=shifts)

@app.get("/shifts/{shift_id}", response_model=schemas.BaseResponse[schemas.Shift])
def read_shift(shift_id: int, db: Session = Depends(get_db)):
    shift = crud.get_shift(db, shift_id=shift_id)
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    return schemas.BaseResponse(data=shift)

@app.post("/user_shifts/", response_model=schemas.BaseResponse[schemas.UserShift])
def create_user_shift(user_shift: schemas.UserShiftCreate, db: Session = Depends(get_db)):
    return schemas.BaseResponse(data=crud.create_user_shift(db=db, user_shift=user_shift))

@app.get("/user_shifts/", response_model=schemas.BaseResponse[List[schemas.UserShift]])
def read_user_shifts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_shifts = crud.get_user_shifts(db, skip=skip, limit=limit)
    return schemas.BaseResponse(data=user_shifts)

@app.get("/user_shifts/user/{user_id}", response_model=schemas.BaseResponse[List[schemas.UserShift]])
def read_user_shifts_by_user(user_id: int, db: Session = Depends(get_db)):
    user_shifts = crud.get_user_shifts_by_user(db, user_id=user_id)
    return schemas.BaseResponse(data=user_shifts)

@app.get("/user_shifts/shift/{shift_id}", response_model=schemas.BaseResponse[List[schemas.UserShift]])
def read_user_shifts_by_shift(shift_id: int, db: Session = Depends(get_db)):
    user_shifts = crud.get_user_shifts_by_shift(db, shift_id=shift_id)
    return schemas.BaseResponse(data=user_shifts)

@app.delete("/user_shifts/{user_shift_id}")
def delete_user_shift(user_shift_id: int, db: Session = Depends(get_db)):
    return schemas.BaseResponse(message=crud.delete_user_shift(db=db, user_shift_id=user_shift_id))

@app.post("/attendances/", response_model=schemas.BaseResponse[schemas.Attendance])
def create_attendance(attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    return schemas.BaseResponse(data=crud.create_attendance(db=db, attendance=attendance))

@app.put("/attendances/{attendance_id}/check_out", response_model=schemas.BaseResponse[schemas.Attendance])
def check_out(attendance_id: int, check_out_lat: float = None, check_out_lng: float = None, check_out_photo: str = None, db: Session = Depends(get_db)):
    return schemas.BaseResponse(data=crud.update_attendance_check_out(db=db, attendance_id=attendance_id, check_out_lat=check_out_lat, check_out_lng=check_out_lng, check_out_photo=check_out_photo))

@app.get("/attendances/", response_model=schemas.BaseResponse[List[schemas.Attendance]])
def read_attendances(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    attendances = crud.get_attendances(db, skip=skip, limit=limit)
    return schemas.BaseResponse(data=attendances)

@app.get("/attendances/{user_id}/{date}", response_model=schemas.BaseResponse[schemas.Attendance])
def read_attendance_by_user_date(user_id: int, date: str, db: Session = Depends(get_db)):
    from datetime import datetime as dt
    attendance_date = dt.strptime(date, "%Y-%m-%d").date()
    return schemas.BaseResponse(data=crud.get_attendance_by_user_date(db, user_id=user_id, date_val=attendance_date))

@app.post("/attendance_logs/", response_model=schemas.BaseResponse[schemas.AttendanceLog])
def create_attendance_log(log: schemas.AttendanceLogCreate, db: Session = Depends(get_db)):
    return schemas.BaseResponse(data=crud.create_attendance_log(db=db, log=log))

@app.get("/attendance_logs/", response_model=schemas.BaseResponse[List[schemas.AttendanceLog]])
def read_attendance_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = crud.get_attendance_logs(db, skip=skip, limit=limit)
    return schemas.BaseResponse(data=logs)

@app.get("/attendance_logs/user/{user_id}", response_model=schemas.BaseResponse[List[schemas.AttendanceLog]])
def read_attendance_logs_by_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = crud.get_attendance_logs_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return schemas.BaseResponse(data=logs)

@app.get("/attendance_logs/{log_id}", response_model=schemas.BaseResponse[schemas.AttendanceLog])
def read_attendance_log(log_id: int, db: Session = Depends(get_db)):
    log = crud.get_attendance_log(db, log_id=log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Attendance log not found")
    return schemas.BaseResponse(data=log)

@app.post("/leave_requests/", response_model=schemas.BaseResponse[schemas.LeaveRequest])
def create_leave_request(leave: schemas.LeaveRequestCreate, db: Session = Depends(get_db)):
    return schemas.BaseResponse(data=crud.create_leave_request(db=db, leave=leave))

@app.get("/leave_requests/", response_model=schemas.BaseResponse[List[schemas.LeaveRequest]])
def read_leave_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    requests = crud.get_leave_requests(db, skip=skip, limit=limit)
    return schemas.BaseResponse(data=requests)

@app.get("/leave_requests/user/{user_id}", response_model=schemas.BaseResponse[List[schemas.LeaveRequest]])
def read_leave_requests_by_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    requests = crud.get_leave_requests_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return schemas.BaseResponse(data=requests)

@app.get("/leave_requests/{request_id}", response_model=schemas.BaseResponse[schemas.LeaveRequest])
def read_leave_request(request_id: int, db: Session = Depends(get_db)):
    request = crud.get_leave_request(db, request_id=request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Leave request not found")
    return schemas.BaseResponse(data=request)

@app.put("/leave_requests/{request_id}/approve", response_model=schemas.BaseResponse[schemas.LeaveRequest])
def approve_leave_request(request_id: int, approved_by: int, db: Session = Depends(get_db)):
    return schemas.BaseResponse(data=crud.approve_leave_request(db=db, request_id=request_id, approved_by=approved_by))

@app.put("/leave_requests/{request_id}/reject", response_model=schemas.BaseResponse[schemas.LeaveRequest])
def reject_leave_request(request_id: int, db: Session = Depends(get_db)):
    return schemas.BaseResponse(data=crud.reject_leave_request(db=db, request_id=request_id))

@app.delete("/leave_requests/{request_id}")
def delete_leave_request(request_id: int, db: Session = Depends(get_db)):
    return schemas.BaseResponse(message=crud.delete_leave_request(db=db, request_id=request_id))