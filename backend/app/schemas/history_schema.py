# history_schema.py
# Defines the shape of JSON data returned by the history endpoints.

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class GestureResultOut(BaseModel):
    id:            int
    gesture_label: str
    confidence:    float
    frame_number:  int

    class Config:
        from_attributes = True

class SessionListItem(BaseModel):
    """Compact representation used in the history list view."""
    id:              int
    video_filename:  Optional[str]
    translated_text: Optional[str]
    avg_confidence:  Optional[float]
    created_at:      datetime

    class Config:
        from_attributes = True

class SessionDetail(BaseModel):
    """Full representation including individual gesture results."""
    id:              int
    video_filename:  Optional[str]
    translated_text: Optional[str]
    avg_confidence:  Optional[float]
    created_at:      datetime
    gesture_results: List[GestureResultOut] = []

    class Config:
        from_attributes = True