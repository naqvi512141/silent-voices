# admin.py
# Admin-only endpoints. Every route here checks that the requesting
# user has role='admin' via the require_admin dependency.
# Regular users receive 403 Forbidden before any logic executes.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import func as sql_func
from datetime import datetime, timedelta
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.session import Session as SessionModel
from app.models.feedback import Feedback
from app.routers.auth import get_current_user
from app.schemas.admin_schema import UserAdminView, SystemStats

router = APIRouter(prefix="/admin", tags=["Admin"])


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency that blocks access unless the authenticated user is an admin.
    Raises HTTP 403 for any user whose role is not 'admin'.
    Inject this into any admin-only endpoint instead of get_current_user.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin privileges required."
        )
    return current_user


# ── User Management ──────────────────────────────────────────────

@router.get("/users", response_model=List[UserAdminView])
def list_all_users(
    admin: User = Depends(require_admin),
    db: DBSession = Depends(get_db)
):
    """Return all registered users ordered by registration date."""
    return db.query(User).order_by(User.created_at.desc()).all()


@router.patch("/users/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    admin: User = Depends(require_admin),
    db: DBSession = Depends(get_db)
):
    """
    Deactivate a user account (soft delete).
    The user will be unable to log in but their data is preserved.
    Admins cannot deactivate themselves.
    """
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="You cannot deactivate your own account.")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = False
    db.commit()
    return {"message": f"User {user.email} has been deactivated."}


@router.patch("/users/{user_id}/activate")
def activate_user(
    user_id: int,
    admin: User = Depends(require_admin),
    db: DBSession = Depends(get_db)
):
    """Reactivate a previously deactivated user account."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = True
    db.commit()
    return {"message": f"User {user.email} has been reactivated."}


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    admin: User = Depends(require_admin),
    db: DBSession = Depends(get_db)
):
    """Permanently delete a user and all their associated data (CASCADE)."""
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="You cannot delete your own account.")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": f"User {user.email} permanently deleted."}


# ── Analytics ────────────────────────────────────────────────────

@router.get("/stats", response_model=SystemStats)
def get_system_stats(
    admin: User = Depends(require_admin),
    db: DBSession = Depends(get_db)
):
    """Return system-wide analytics for the admin dashboard."""
    total_users    = db.query(sql_func.count(User.id)).scalar()
    total_sessions = db.query(sql_func.count(SessionModel.id)).scalar()
    
    # AVG returns None if there are no sessions — default to 0.0
    avg_conf_raw = db.query(
        sql_func.avg(SessionModel.avg_confidence)
    ).scalar()
    avg_confidence = round(float(avg_conf_raw), 1) if avg_conf_raw else 0.0
    
    # Sessions created in the last 7 days
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    sessions_last_7days = db.query(sql_func.count(SessionModel.id)).filter(
        SessionModel.created_at >= seven_days_ago
    ).scalar()
    
    return SystemStats(
        total_users=total_users,
        total_sessions=total_sessions,
        avg_confidence=avg_confidence,
        sessions_last_7days=sessions_last_7days
    )


@router.get("/sessions")
def list_all_sessions(
    admin: User = Depends(require_admin),
    db: DBSession = Depends(get_db)
):
    """Return all sessions across all users for admin monitoring."""
    sessions = (
        db.query(SessionModel)
        .order_by(SessionModel.created_at.desc())
        .limit(100)  # Limit to last 100 to avoid performance issues
        .all()
    )
    return [
        {
            "id": s.id,
            "user_id": s.user_id,
            "translated_text": s.translated_text,
            "avg_confidence": s.avg_confidence,
            "created_at": s.created_at.isoformat()
        }
        for s in sessions
    ]