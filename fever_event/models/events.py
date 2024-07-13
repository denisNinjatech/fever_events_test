from sqlalchemy import Column, Integer, String, DateTime, func
from fever_event.db.database import Base

# Events Table
class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    base_event_id = Column(Integer, index=True)
    event_id = Column(Integer, index=True)
    title = Column(String(255))
    start_datetime = Column(DateTime, index=True)
    end_datetime = Column(DateTime, index=True)
    min_price = Column(Integer)
    max_price = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())