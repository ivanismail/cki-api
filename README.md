# Attendance API

A FastAPI-based attendance system.

## Installation

1. Create virtual environment: `python -m venv venv`

2. Activate venv: `.\venv\Scripts\activate` (Windows)

3. Install dependencies: `pip install -r requirements.txt`

4. Run the server: `uvicorn app.main:app --reload` or use VS Code task "Run FastAPI Server"

## API Endpoints

- GET / : Welcome message

- POST /users/ : Create a new user (JSON: {"name": "string", "email": "string"})

- GET /users/ : List all users

- POST /attendances/ : Check in (JSON: {"user_id": int})

- PUT /attendances/{attendance_id}/check_out : Check out

- GET /attendances/ : List all attendances

## Database

Uses SQLite database `attendance.db` created automatically.

Tables: users, attendances