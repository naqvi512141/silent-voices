# user.py — Defines the 'users' table as a Python class
# SQLAlchemy will look at this class and create the matching database table

from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base  # Inherit from Base to register as a table

class User(Base):
    # This tells SQLAlchemy the name of the actual table in the database
    __tablename__ = "users"

    # Each Column() call defines one column in the table
    
    # id is the primary key — a unique number that identifies each row
    # autoincrement=True means PostgreSQL assigns it automatically (1, 2, 3, ...)
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Full name — up to 100 characters, required (nullable=False)
    full_name = Column(String(100), nullable=False)
    
    # Email — must be unique across all users, required
    email = Column(String(150), unique=True, nullable=False)
    
    # NEVER store plain text passwords — only the bcrypt hash
    hashed_password = Column(String(255), nullable=False)
    
    # Role is either 'user' or 'admin' — default is 'user'
    role = Column(String(10), default="user")
    
    # created_at is set automatically to the current time when a row is inserted
    created_at = Column(DateTime, server_default=func.now())