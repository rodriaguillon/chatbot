from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except ValidationError as ve:
        return JSONResponse(status_code=422, content={"error": "Input validation failed.", "details": ve.errors()})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal server error."})
