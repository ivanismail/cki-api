from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from .schemas import BaseResponse

def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseResponse(
            success=False,
            message=exc.detail
        ).model_dump()
    )
