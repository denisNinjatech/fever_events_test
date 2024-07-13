from pydantic import BaseModel
from datetime import datetime
from typing import List,Optional,Dict
import uuid


# Events Base Schema
class EventsBaseSchema(BaseModel):
    title: str
    start_datetime: datetime
    end_datetime: datetime
    min_price: int
    max_price: int
    event_id: str

# Events Create Schema
class EventsCreateSchema(EventsBaseSchema):
    base_event_id: str

# Events Get Schema
class EventResponseData(BaseModel):
    id: uuid.UUID
    title: str
    start_date: str
    start_time: str
    end_date: str
    end_time: str
    min_price: int
    max_price: int

class EventListResponse(BaseModel):
    data: Dict[str, List[EventResponseData]]
    error: Optional[str] = None  # Allow None as a default value
   
   
class ErrorDetails(BaseModel):
    code: str
    message: str

class ErrorResponse(BaseModel):
    error: ErrorDetails
    data: Optional[Dict] = None