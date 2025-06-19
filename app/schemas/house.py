# app/schemas/house.py

from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

class HouseCreate(BaseModel):
    user_id: int
    address: Optional[str] = None
    area_sqm: Decimal
    room_count: Optional[int] = None

class House(BaseModel):
    id: int
    user_id: int
    address: Optional[str]
    area_sqm: Decimal
    room_count: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True
