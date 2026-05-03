from pydantic import BaseModel
from datetime import datetime

class UserAdminView(BaseModel):
    """What the admin sees when listing all users."""
    id:         int
    full_name:  str
    email:      str
    role:       str
    is_active:  bool
    created_at: datetime

    class Config:
        from_attributes = True

class SystemStats(BaseModel):
    total_users:         int
    total_sessions:      int
    avg_confidence:      float
    sessions_last_7days: int