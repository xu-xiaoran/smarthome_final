# app/schemas/device.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DeviceCreate(BaseModel):
    house_id: int
    device_name: str
    device_type: str
    location: Optional[str] = None
    model: Optional[str] = None

class Device(BaseModel):
    id: int
    house_id: int
    device_name: str
    device_type: str
    location: Optional[str]
    model: Optional[str]
    added_at: datetime

    class Config:
        orm_mode = True
