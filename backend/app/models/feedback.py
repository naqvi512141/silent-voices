# feedback.py
# Stores user ratings on translation quality.
# One session can have at most one feedback record (unique constraint on session_id).
# This is the "human in the loop" data collection discussed in the proposal.

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    
    # unique=True enforces one feedback per session — prevents duplicate submissions
    session_id   = Column(Integer,
                          ForeignKey("sessions.id", ondelete="CASCADE"),
                          nullable=False,
                          unique=True)
    
    # 1 = thumbs up (correct translation), 0 = thumbs down (incorrect)
    rating       = Column(Integer, nullable=False)
    
    # Optional: the user types what the correct translation should have been.
    # This is the correction data that would be used to retrain the model later.
    correction   = Column(Text, nullable=True)
    
    submitted_at = Column(DateTime, server_default=func.now())
    
    session      = relationship("Session", back_populates="feedback")