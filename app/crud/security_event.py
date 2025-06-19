# app/crud/security_event.py

from sqlalchemy.orm import Session
from app.models.security_event import SecurityEvent
from app.schemas.security_event import SecurityEventCreate
from typing import List, Optional

def get_security_event_by_id(db: Session, event_id: int) -> Optional[SecurityEvent]:
    return db.query(SecurityEvent).filter(SecurityEvent.id == event_id).first()

def get_security_events_by_house(db: Session, house_id: int) -> List[SecurityEvent]:
    return db.query(SecurityEvent).filter(SecurityEvent.house_id == house_id).all()

def create_security_event(db: Session, event: SecurityEventCreate) -> SecurityEvent:
    db_event = SecurityEvent(
        house_id=event.house_id,
        device_id=event.device_id,
        event_type=event.event_type,
        event_time=event.event_time,
        description=event.description
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_security_event(db: Session, event_id: int) -> bool:
    ev = db.query(SecurityEvent).filter(SecurityEvent.id == event_id).first()
    if not ev:
        return False
    db.delete(ev)
    db.commit()
    return True

def update_security_event_handle(db: Session, event_id: int, is_handled: bool, feedback_id: Optional[int] = None) -> Optional[SecurityEvent]:
    ev = db.query(SecurityEvent).filter(SecurityEvent.id == event_id).first()
    if not ev:
        return None
    ev.is_handled = is_handled
    ev.feedback_id = feedback_id
    db.commit()
    db.refresh(ev)
    return ev
