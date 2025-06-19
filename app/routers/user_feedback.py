# app/routers/user_feedback.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/user_feedbacks",
    tags=["user_feedbacks"],
)

@router.post("/", response_model=schemas.user_feedback.UserFeedback, status_code=status.HTTP_201_CREATED)
def create_user_feedback(feedback: schemas.user_feedback.UserFeedbackCreate, db: Session = Depends(get_db)):
    # 检查用户是否存在
    db_user = crud.user.get_user_by_id(db, feedback.user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    # 如果传了 event_id，需要检查事件是否存在
    if feedback.event_id:
        db_event = crud.security_event.get_security_event_by_id(db, feedback.event_id)
        if not db_event:
            raise HTTPException(status_code=404, detail="关联事件不存在")
    return crud.user_feedback.create_user_feedback(db, feedback)

@router.get("/{feedback_id}", response_model=schemas.user_feedback.UserFeedback)
def read_user_feedback(feedback_id: int, db: Session = Depends(get_db)):
    fb = crud.user_feedback.get_feedback_by_id(db, feedback_id)
    if not fb:
        raise HTTPException(status_code=404, detail="反馈不存在")
    return fb

@router.get("/by_user/{user_id}", response_model=List[schemas.user_feedback.UserFeedback])
def list_feedbacks_by_user(user_id: int, db: Session = Depends(get_db)):
    return crud.user_feedback.get_feedbacks_by_user(db, user_id)

@router.delete("/{feedback_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_feedback(feedback_id: int, db: Session = Depends(get_db)):
    success = crud.user_feedback.delete_user_feedback(db, feedback_id)
    if not success:
        raise HTTPException(status_code=404, detail="反馈不存在")
    return

@router.put("/{feedback_id}", response_model=schemas.user_feedback.UserFeedback)
def update_user_feedback(feedback_id: int, feedback_update: schemas.user_feedback.UserFeedbackCreate, db: Session = Depends(get_db)):
    db_fb = crud.user_feedback.get_feedback_by_id(db, feedback_id)
    if not db_fb:
        raise HTTPException(status_code=404, detail="反馈不存在")
    update_data = feedback_update.dict(exclude_unset=True)
    fb_obj = crud.user_feedback.update_feedback(db, feedback_id, **update_data)
    return fb_obj
