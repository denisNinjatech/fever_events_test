from fever_event.db.database import engine, Base
from fever_event.models import events

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()