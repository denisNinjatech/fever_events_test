from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from decouple import AutoConfig
import os

# Set up the base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
config = AutoConfig(search_path=BASE_DIR)

# MySQL Database Connection
username = config("DB_USERNAME")
password = quote_plus(config("DB_PASSWORD"))  # URL-encoded password
host = config("DB_HOST")  # or the host of your MySQL server
port = config("DB_PORT")  # default MySQL port
database_name = config("DB_DATABASE_NAME")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()