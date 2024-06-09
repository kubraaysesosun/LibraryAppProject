import traceback

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi_pagination import add_pagination
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from app.config import settings
from app.database.core import SessionLocal
from app.schemas.base_schema import ErrorData, ResponseSchema
from app.views.v1.endpoins.books import router as library_router
from app.views.v1.endpoins.auth import router as auth_router

app = FastAPI(
    title="Api",
    version="1",
    swagger_ui_parameters={"docExpansion": "none"},
)
app.include_router(library_router, prefix="/books", tags=["Books"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
add_pagination(app)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    if isinstance(exc.detail, str):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error_code": exc.status_code,
                "error_message": exc.detail,
            },
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.detail.value,
            "error_message": exc.detail.phrase,
        },
    )


@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        request.state.db = SessionLocal()
        return await call_next(request)
    except Exception:
        if settings.DEVELOPER_MODE:
            traceback.print_exc()
        request.state._exception = traceback.format_exc()
        return JSONResponse(
            status_code=500,
            content=ResponseSchema(
                success=False,
                error=ErrorData(code=500, message="Internal server error"),
                data=None,
            ).dict(),
        )
    finally:
        request.state.db.close()


@app.exception_handler(ValidationError)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ResponseSchema(
            success=False,
            message="Validation Error",
            error=ErrorData(
                code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                message="Validation Error",
                fields={
                    ".".join([str(x) for x in error["loc"][1:]]): error["msg"]
                    for error in exc.errors()
                },
            ),
            data=None,
        ).dict(),
    )
