# app/schemas/user_feedback.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserFeedbackCreate(BaseModel):
    user_id: int
    event_id: Optional[int] = None
    feedback_text: str
    feedback_type: Optional[str] = None

class UserFeedback(BaseModel):
    id: int
    user_id: int
    event_id: Optional[int]
    feedback_text: str
    feedback_time: datetime
    feedback_type: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
