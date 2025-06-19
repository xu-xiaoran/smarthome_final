# app/schemas/usage_record.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta

class UsageRecordCreate(BaseModel):
    device_id: int
    user_id: int
    action: str
    start_time: datetime
    end_time: Optional[datetime] = None  # 如果当次操作有结束时间，可以传；否则可先插入 start_time，后续更新

class UsageRecord(BaseModel):
    id: int
    device_id: int
    user_id: int
    action: str
    start_time: datetime
    end_time: Optional[datetime]
    usage_duration: Optional[timedelta]
    created_at: datetime

    class Config:
        orm_mode = True
