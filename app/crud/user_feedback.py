# app/crud/user_feedback.py

from sqlalchemy.orm import Session
from app.models.user_feedback import UserFeedback
from app.schemas.user_feedback import UserFeedbackCreate
from typing import List, Optional

def get_feedback_by_id(db: Session, feedback_id: int) -> Optional[UserFeedback]:
    return db.query(UserFeedback).filter(UserFeedback.id == feedback_id).first()

def get_feedbacks_by_user(db: Session, user_id: int) -> List[UserFeedback]:
    return db.query(UserFeedback).filter(UserFeedback.user_id == user_id).all()

def create_user_feedback(db: Session, feedback: UserFeedbackCreate) -> UserFeedback:
    db_fb = UserFeedback(
        user_id=feedback.user_id,
        event_id=feedback.event_id,
        feedback_text=feedback.feedback_text,
        feedback_type=feedback.feedback_type
    )
    db.add(db_fb)
    db.commit()
    db.refresh(db_fb)
    return db_fb

def delete_user_feedback(db: Session, feedback_id: int) -> bool:
    fb = db.query(UserFeedback).filter(UserFeedback.id == feedback_id).first()
    if not fb:
        return False
    db.delete(fb)
    db.commit()
    return True

def update_feedback(db: Session, feedback_id: int, **kwargs) -> Optional[UserFeedback]:
    fb = db.query(UserFeedback).filter(UserFeedback.id == feedback_id).first()
    if not fb:
        return None
    for key, value in kwargs.items():
        setattr(fb, key, value)
    db.commit()
    db.refresh(fb)
    return fb
