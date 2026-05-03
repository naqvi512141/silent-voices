# feedback.py
# Handles thumbs-up/down ratings and correction submissions after translation.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DBSession

from app.database import get_db
from app.models.feedback import Feedback
from app.models.session import Session as SessionModel
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.feedback_schema import FeedbackCreate, FeedbackResponse

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("/{session_id}", response_model=FeedbackResponse, status_code=201)
def submit_feedback(
    session_id: int,
    data: FeedbackCreate,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    """
    Submit a thumbs-up (rating=1) or thumbs-down (rating=0) for a session.
    An optional correction string can be provided when rating=0.
    Each session can have at most one feedback record.
    """
    # Verify the session exists and belongs to this user
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Check if feedback already exists for this session
    existing = db.query(Feedback).filter(
        Feedback.session_id == session_id
    ).first()
    
    if existing:
        # Update the existing feedback instead of creating a duplicate
        existing.rating = data.rating
        existing.correction = data.correction
        db.commit()
        db.refresh(existing)
        return existing
    
    # Create new feedback record
    new_feedback = Feedback(
        session_id=session_id,
        rating=data.rating,
        correction=data.correction
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback