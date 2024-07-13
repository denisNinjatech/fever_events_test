import requests
import pytz
from io import BytesIO
from lxml import etree
from datetime import datetime
from celery import shared_task
from sqlalchemy.orm import Session
from typing import List
from fever_event.db.database import SessionLocal
from fever_event.models.events import Events
from fever_event.celery import celery_app
from fever_event.schemas.events import EventsCreateSchema

# Fetch Events data in XML formate from the provider API
def fetch_events() -> bytes:
    EXTERNAL_API_URL = "https://provider.code-challenge.feverup.com/api/events"
    try:
        response = requests.get(EXTERNAL_API_URL)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Error fetching events: {e}")
        return b""

# Normalized Data provided by provider API as per our requirements
def normalize_events(xml_string: bytes) -> List[EventsCreateSchema]:
    events = []
    
    xml_bytes = BytesIO(xml_string)
    context = etree.iterparse(
        xml_bytes,
        events=("end",),
        tag="base_event",
        recover=True,
    )
    
    for _, elem in context:
        sell_mode = elem.get("sell_mode")
        base_event_id = elem.get("base_event_id")
        if sell_mode == "online":
            title = elem.get("title")
            for event in elem.findall("event"):
                event_id = event.get("event_id")
                start_date_time = event.get("event_start_date")
                end_date_time = event.get("event_end_date")
                
                starts_at = datetime.fromisoformat(start_date_time)
                ends_at = datetime.fromisoformat(end_date_time)
                prices = [float(zone.get("price")) for zone in event.findall("zone")]
                min_price = min(prices) if prices else None
                max_price = max(prices) if prices else None
                
                event_obj = EventsCreateSchema(
                    base_event_id=base_event_id,
                    event_id=event_id,
                    title=title,
                    start_datetime=starts_at,
                    end_datetime=ends_at,
                    min_price=int(min_price) if min_price is not None else None,
                    max_price=int(max_price) if max_price is not None else None,
                )
                events.append(event_obj)
        
        # Clean Up The Memory Space Occupied By Current Elment
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    
    return events


# Store the Event Data in Our Database
def store_events(events: List[EventsCreateSchema]):
    db: Session = SessionLocal()
    kolkata_tz = pytz.timezone('Asia/Kolkata')
    try:
        for event in events:
            try:
                # Check if the event already exists in the database
                existing_event = db.query(Events).filter_by(
                    base_event_id=event.base_event_id,
                    event_id=event.event_id,
                    start_datetime=event.start_datetime,
                    end_datetime=event.end_datetime
                ).first()
                
                if existing_event:
                    # Update the existing event's start and end datetime
                    existing_event.updated_at = datetime.now(kolkata_tz)  # Explicitly update the updated_at field
                    db.commit()
                    print(f"Updated event: {existing_event}")
                else:
                    # Create a new event
                    new_event = Events(**event.dict())
                    db.add(new_event)
                    db.commit()
                    print(f"Created new event: {new_event}")
                    
            except Exception as e:
                db.rollback()
                print(f"Error processing event: {e}")
    except Exception as e:
        print(f"Error storing events: {e}")
    finally:
        db.close()


# Celery Schedule task to call the provider API in 1 minutes interval
@shared_task
def scheduled_fetch():
    data = fetch_events()
    if data:
        events = normalize_events(data)
        store_events(events)