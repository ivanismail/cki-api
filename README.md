# Attendance API

A FastAPI-based attendance system with standardized responses and comprehensive error handling.

## Installation

1. Create virtual environment: `python -m venv venv`

2. Activate venv: `.\venv\Scripts\activate` (Windows)

3. Install dependencies: `pip install -r requirements.txt`

4. Create a `.env` file with your MySQL connection string or MySQL credentials.

   Either:

   ```
   SQLALCHEMY_DATABASE_URL=mysql+pymysql://username:password@hostname:3306/database_name
   ```

   Or:

   ```
   DB_USER=username
   DB_PASSWORD=password
   DB_HOST=hostname
   DB_PORT=3306
   DB_NAME=database_name
   ```

5. Run the server: `uvicorn app.main:app --reload` or use VS Code task "Run FastAPI Server"

## Response Format

All API responses follow a standardized format using `BaseResponse`:

```json
{
  "success": true,
  "message": "optional message",
  "data": {}
}
```

Error responses:

```json
{
  "success": false,
  "message": "Error description",
  "data": null
}
```

## Exception Handling

The API includes centralized exception handling that automatically wraps HTTPExceptions in the BaseResponse format for consistent error responses across all endpoints.

## API Endpoints

### Authentication

- POST /token : Login with credentials, returns access token

### Users

- POST /users/ : Create a new user
- GET /users/ : List all users (paginated)
- GET /users/me : Get current authenticated user

### Shifts

- POST /shifts/ : Create a shift
- GET /shifts/ : List all shifts (paginated)
- GET /shifts/{shift_id} : Get shift by ID

### User Shifts

- POST /user_shifts/ : Assign shift to user
- GET /user_shifts/ : List all user-shift assignments
- GET /user_shifts/user/{user_id} : Get shifts for a user
- GET /user_shifts/shift/{shift_id} : Get users for a shift
- DELETE /user_shifts/{user_shift_id} : Remove user-shift assignment

### Attendance

- POST /attendances/ : Create attendance record (check-in)
- GET /attendances/ : List all attendance records (paginated)
- GET /attendances/{user_id}/{date} : Get attendance for user on specific date
- GET /attendances/me/history : Get authenticated user's attendance history (paginated, requires token)
- PUT /attendances/{attendance_id}/check_out : Update attendance check-out

### Attendance Logs

- POST /attendance_logs/ : Create attendance log
- GET /attendance_logs/ : List all logs (paginated)
- GET /attendance_logs/user/{user_id} : Get logs for specific user
- GET /attendance_logs/me/history : Get authenticated user's attendance logs history (paginated, requires token)
- GET /attendance_logs/{log_id} : Get specific log

### Leave Requests

- POST /leave_requests/ : Create leave request
- GET /leave_requests/ : List all leave requests (paginated)
- GET /leave_requests/user/{user_id} : Get leave requests for user
- GET /leave_requests/{request_id} : Get specific leave request
- PUT /leave_requests/{request_id}/approve : Approve leave request
- PUT /leave_requests/{request_id}/reject : Reject leave request
- DELETE /leave_requests/{request_id} : Delete leave request

## Database

Uses SQLAlchemy ORM with support for MySQL and SQLite databases.

Tables: users, shifts, user_shifts, attendances, attendance_logs, leave_requests
