from fastapi import APIRouter, Query
from sqlalchemy.orm import Session
from fever_event.db.database import SessionLocal
from datetime import datetime
from fever_event.models.events import Events
from typing import  Optional
from fever_event.schemas.events import EventListResponse,EventResponseData,ErrorResponse,ErrorDetails
import uuid
from fastapi.responses import JSONResponse
from event_log_config import logger

router = APIRouter()

# API GET Route to Get all the events data between starts_at and ends_at
@router.get(
    "/search", 
    summary="Lists the available events on a time range",
    tags=["default"],
    responses={
        200: {"model": EventListResponse, "description": "List of plans"},
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Generic error"},
    }
)
def read_events(
    starts_at: Optional[datetime] = Query(None, description="Return only events that start after this date"),
    ends_at: Optional[datetime] = Query(None, description="Return only events that finish before this date")
):
    db: Session = SessionLocal()
    try:
    
        query = db.query(Events)

        # Apply filters if starts_at or ends_at are provided
        if starts_at:
            query = query.filter(Events.start_datetime >= starts_at)
        if ends_at:
            query = query.filter(Events.end_datetime <= ends_at)

        # Execute query and fetch all events
        events = query.all()

        # Serialize events to EventResponseData using list comprehension
        events_data = [
            EventResponseData(
                id=str(uuid.uuid4()),
                title=event.title,
                start_date=event.start_datetime.date().isoformat(),
                start_time=event.start_datetime.time().isoformat(),
                end_date=event.end_datetime.date().isoformat(),
                end_time=event.end_datetime.time().isoformat(),
                min_price=event.min_price,
                max_price=event.max_price
            )
            for event in events
        ]

        return EventListResponse(status_code=200,data={"events": events_data}, error=None)
    except ValueError as e:
        logger.error(f"ValueError: {str(e)}")
        error_data = ErrorResponse(
            error=ErrorDetails(code="400", message=str(e)),
            data=None
        )
        return JSONResponse(status_code=400, content=error_data.dict())
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        error_data = ErrorResponse(
            error=ErrorDetails(code="500", message=str(e)),
            data=None
        )
        return JSONResponse(status_code=500, content=error_data.dict())
    finally:
        db.close()
