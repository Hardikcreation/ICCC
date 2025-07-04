from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Use DATABASE_URL from your .env file
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine without SQLite-specific options
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
