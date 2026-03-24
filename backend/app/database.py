# database.py — This file sets up the connection between your Python code and PostgreSQL

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load the .env file so os.getenv() can read itbackend/venv/Scripts/python.exe
load_dotenv()

# Get the database URL from your .env file
# This string tells SQLAlchemy WHERE the database is and HOW to connect
DATABASE_URL = os.getenv("DATABASE_URL")

# --- ADD THIS LINE FOR TESTING ---
print(f"DEBUG: My Database URL is: {DATABASE_URL}")
# ---------------------------------

# The "engine" is the actual connection to the database
# It is like the telephone line to PostgreSQL
engine = create_engine(DATABASE_URL)

# A "session" is like one conversation with the database
# SessionLocal is a factory — calling SessionLocal() creates a new session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class for all your database table definitions
# When you define a table (like User), it inherits from Base
Base = declarative_base()

# This is a "dependency" — a function FastAPI calls automatically
# to give each endpoint its own fresh database session
def get_db():
    db = SessionLocal()  # Open a new session (start a conversation with the DB)
    try:
        yield db          # Give the session to the endpoint that needs it
    finally:
        db.close()        # Always close the session when done, no matter what