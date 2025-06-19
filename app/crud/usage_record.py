# app/crud/usage_record.py

from sqlalchemy.orm import Session
from app.models.usage_record import UsageRecord
from app.schemas.usage_record import UsageRecordCreate
from typing import List, Optional
from datetime import datetime

def get_usage_record_by_id(db: Session, record_id: int) -> Optional[UsageRecord]:
    return db.query(UsageRecord).filter(UsageRecord.id == record_id).first()

def get_usage_records_by_device(db: Session, device_id: int) -> List[UsageRecord]:
    return db.query(UsageRecord).filter(UsageRecord.device_id == device_id).all()

def get_usage_records_by_user(db: Session, user_id: int) -> List[UsageRecord]:
    return db.query(UsageRecord).filter(UsageRecord.user_id == user_id).all()

def create_usage_record(db: Session, record: UsageRecordCreate) -> UsageRecord:
    # 计算 usage_duration，如果传入了 end_time
    duration = None
    if record.end_time:
        duration = record.end_time - record.start_time

    db_record = UsageRecord(
        device_id=record.device_id,
        user_id=record.user_id,
        action=record.action,
        start_time=record.start_time,
        end_time=record.end_time,
        usage_duration=duration
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def delete_usage_record(db: Session, record_id: int) -> bool:
    rec = db.query(UsageRecord).filter(UsageRecord.id == record_id).first()
    if not rec:
        return False
    db.delete(rec)
    db.commit()
    return True

def update_usage_record(db: Session, record_id: int, end_time: datetime) -> Optional[UsageRecord]:
    rec = db.query(UsageRecord).filter(UsageRecord.id == record_id).first()
    if not rec:
        return None
    rec.end_time = end_time
    rec.usage_duration = end_time - rec.start_time
    db.commit()
    db.refresh(rec)
    return rec
