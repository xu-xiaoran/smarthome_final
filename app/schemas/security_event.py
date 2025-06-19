# app/schemas/security_event.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SecurityEventCreate(BaseModel):
    house_id: int
    device_id: Optional[int] = None
    event_type: str
    event_time: datetime
    description: Optional[str] = None

class SecurityEvent(BaseModel):
    id: int
    house_id: int
    device_id: Optional[int]
    event_type: str
    event_time: datetime
    description: Optional[str]
    is_handled: bool
    created_at: datetime

    class Config:
        orm_mode = True
