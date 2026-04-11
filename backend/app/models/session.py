# session.py — Stores each translation session and its per-gesture results.
# One session = one uploaded video = one translation event.
# A session has many gesture results (one row per recognised gesture in the video).

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Which user uploaded this video?
    # ForeignKey links this table to the users table.
    # If the user is deleted, their sessions are also deleted (CASCADE).
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    video_filename = Column(String(255))          # Name of the uploaded file
    translated_text = Column(Text)                # Final assembled sentence
    avg_confidence = Column(Float)                # Average confidence across all gestures
    created_at = Column(DateTime, server_default=func.now())

    # 'relationship' lets you do session.gesture_results to get all related rows
    gesture_results = relationship("GestureResult", back_populates="session",
                                   cascade="all, delete-orphan")
    user = relationship("User", back_populates="sessions")


class GestureResult(Base):
    __tablename__ = "gesture_results"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    gesture_label = Column(String(50))  # e.g. "A", "Hello", "Thank You"
    confidence = Column(Float)          # e.g. 0.87 (87%)
    frame_number = Column(Integer)      # Which frame in the video this came from

    session = relationship("Session", back_populates="gesture_results")