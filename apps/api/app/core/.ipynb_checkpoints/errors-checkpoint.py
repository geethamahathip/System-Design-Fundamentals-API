from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import uuid
#unified error builder
def build_error(code: str, message: str, request_id: str):
    return {
        "error": {
            "code": code,
            "message": message,
            "request_id": request_id
        }
    }
#http exception handler 4xx
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))

    if exc.status_code == 401:
        code = "AUTH_ERROR"
    elif exc.status_code == 404:
        code = "NOT_FOUND"
    elif exc.status_code == 422:
        code = "VALIDATION_ERROR"
    else:
        code = "CLIENT_ERROR"

    return JSONResponse(
        status_code=exc.status_code,
        content=build_error(code, str(exc.detail), request_id),
    )
#validation error handling
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))

    # DO NOT leak internal validation structure
    return JSONResponse(
        status_code=422,
        content=build_error(
            code="VALIDATION_ERROR",
            message="Invalid request payload",
            request_id=request_id,
        ),
    )
#global 5xx handler
async def global_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))

    return JSONResponse(
        status_code=500,
        content=build_error(
            code="INTERNAL_SERVER_ERROR",
            message="Something went wrong. Please try again later.",
            request_id=request_id,
        ),
    )