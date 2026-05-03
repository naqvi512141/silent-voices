# user.py
# Sprint 3 change: added is_active column so admins can deactivate accounts
# without permanently deleting them (safer approach in production systems).

from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    full_name       = Column(String(100), nullable=False)
    email           = Column(String(150), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role            = Column(String(10), default="user")
    
    # is_active allows admins to deactivate accounts without hard-deleting them.
    # Deactivated users cannot log in. Defaults to True for all new accounts.
    is_active       = Column(Boolean, default=True, nullable=False)
    
    created_at      = Column(DateTime, server_default=func.now())
    
    sessions        = relationship("Session", back_populates="user",
                                   cascade="all, delete-orphan")