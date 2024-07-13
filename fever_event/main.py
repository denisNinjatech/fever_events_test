from fastapi import FastAPI, Request,status
from fever_event.api import events
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from event_log_config import logger
# FastAPI App Initialize
app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    detail = [{"loc": e["loc"], "msg": e["msg"], "type": e["type"]} for e in errors]
    logger.error(f"RequestValidationError: {detail}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,  # Change status code to 400
        content={
            "error": {
                "code": "400",
                "message": "Validation Error",
                # "detail": detail
            },
            "data": None
        }
    )


# Include All the available REST API routes
app.include_router(events.router)

# Start FastAPI App
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
