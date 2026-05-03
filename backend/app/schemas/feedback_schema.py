from pydantic import BaseModel, field_validator
from typing import Optional

class FeedbackCreate(BaseModel):
    rating:     int            # Must be 0 or 1
    correction: Optional[str] = None

    @field_validator("rating")
    @classmethod
    def rating_must_be_binary(cls, v):
        if v not in (0, 1):
            raise ValueError("Rating must be 0 (incorrect) or 1 (correct)")
        return v

class FeedbackResponse(BaseModel):
    id:         int
    session_id: int
    rating:     int
    correction: Optional[str]

    class Config:
        from_attributes = True